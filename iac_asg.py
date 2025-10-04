import boto3
import base64

# ------------------ CONFIG ------------------
REGION = "us-west-2"
AMI_ID = "ami-0ec1bf4a8f92e7bd1"       # Ubuntu 20.04 LTS (check latest in us-west-2)
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "Jigar_New_Key"              # update with your EC2 key pair name
SECURITY_GROUP = "sg-01fa05790aa51e240"         # SG ID in the same VPC as your subnets
IAM_INSTANCE_PROFILE = "jigar-EC2-SSM-Role-Autodelete"  # IAM role name with ECR + EC2 perms
SUBNETS = ["subnet-03ca36de9a927fe8e", "subnet-09bd0e0acc92d4efa"]  # public subnets in same VPC


ACCOUNT_ID = "975050024946"

                # your AWS account ID
TG_ARN_FRONTEND = "arn:aws:elasticloadbalancing:us-west-2:975050024946:targetgroup/tg-frontend-service-v3/abf91a8df11c8d13"
TG_ARN_HELLO = "arn:aws:elasticloadbalancing:us-west-2:975050024946:targetgroup/tg-hello-service-v3/8db7e73110675adb"
TG_ARN_PROFILE = "arn:aws:elasticloadbalancing:us-west-2:975050024946:targetgroup/tg-profile-service-v3/12d26c04ad2f32ff"


# ------------------ BOTO3 CLIENTS ------------------
ec2 = boto3.client("ec2", region_name=REGION)
autoscaling = boto3.client("autoscaling", region_name=REGION)

# ------------------ USER DATA TEMPLATES ------------------
USERDATA_TEMPLATE = """#!/bin/bash
set -xe

# Install dependencies
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker GPG key & repo

sudo curl -fsSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker

# Now AWS CLI

sudo apt install -y unzip curl
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Login to ECR
aws ecr get-login-password --region us-west-2 | sudo docker login --username AWS --password-stdin 975050024946.dkr.ecr.us-west-2.amazonaws.com

# Pull + Run container
sudo docker pull {account_id}.dkr.ecr.{region}.amazonaws.com/{service_name}:latest
sudo docker run -d -p {host_port}:{container_port} {account_id}.dkr.ecr.{region}.amazonaws.com/{service_name}:latest
"""

# ------------------ FUNCTION TO CREATE LAUNCH TEMPLATE + ASG ------------------
def create_lt_asg(service_name, lt_name, asg_name, tg_arn, host_port, container_port):
    """Creates Launch Template + Auto Scaling Group"""
    print(f"🚀 Creating {service_name}...")

    userdata_script = USERDATA_TEMPLATE.format(
        region=REGION,
        account_id=ACCOUNT_ID,
        service_name=service_name,
         host_port=host_port,
        container_port=container_port
    )

    # Encode userdata
    userdata_encoded = base64.b64encode(userdata_script.encode("utf-8")).decode("utf-8")

    # Create Launch Template
    lt = ec2.create_launch_template(
        LaunchTemplateName=lt_name,
        LaunchTemplateData={
            "ImageId": AMI_ID,
            "InstanceType": INSTANCE_TYPE,
            "KeyName": KEY_NAME,
            "SecurityGroupIds": [SECURITY_GROUP],
            "IamInstanceProfile": {"Name": IAM_INSTANCE_PROFILE},
            "UserData": userdata_encoded,
        },
    )

    # Create ASG with Target Group attached
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={"LaunchTemplateName": lt_name, "Version": "$Latest"},
        MinSize=1,
        MaxSize=2,
        DesiredCapacity=1,
        VPCZoneIdentifier=",".join(SUBNETS),
        TargetGroupARNs=[tg_arn],
        HealthCheckType="EC2",
        HealthCheckGracePeriod=60
    )

    print(f"✅ Created ASG {asg_name} with LT {lt_name} and attached to TG {tg_arn}✅")

# ------------------ Create All 3 Services ------------------
# Profile service (port 7202:7202)
create_lt_asg("jigar-profile-service", "jigar-profile-lt", "jigar-profile-asg",
              TG_ARN_PROFILE, 7202, 7202)

# Hello service (port 7201:7201)
create_lt_asg("jigar-hello-service", "jigar-hello-lt", "jigar-hello-asg",
              TG_ARN_HELLO, 7201, 7201)

# Frontend service (map host 3000 → container 80)
create_lt_asg("jigar-frontend-hp", "jigar-frontend-lt", "jigar-frontend-asg",
              TG_ARN_FRONTEND, 3000, 80)
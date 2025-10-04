import boto3

ec2 = boto3.client('ec2', region_name='us-west-2')
elbv2 = boto3.client('elbv2', region_name='us-west-2')
autoscaling = boto3.client('autoscaling', region_name='us-west-2')

VPC_ID = "vpc-0321f38a7b594180d"
SUBNETS = ["subnet-03ca36de9a927fe8e", "subnet-09bd0e0acc92d4efa"]   # at least 2 AZs
SG_ID = "sg-01fa05790aa51e240"                     # Security Group allowing 80 inbound

def create_alb():
    alb = elbv2.create_load_balancer(
        Name="jigar-alb",
        Subnets=SUBNETS,
        SecurityGroups=[SG_ID],
        Scheme="internet-facing",
        Type="application",
        IpAddressType="ipv4"
    )
    alb_arn = alb["LoadBalancers"][0]["LoadBalancerArn"]
    print("✅ ALB Created:", alb_arn)
    return alb_arn

def create_target_group(name, port):
    tg = elbv2.create_target_group(
        Name=name,
        Protocol="HTTP",
        Port=port,
        VpcId=VPC_ID,
        TargetType="instance"
    )
    tg_arn = tg["TargetGroups"][0]["TargetGroupArn"]
    print(f"✅ Target Group {name} Created:", tg_arn)
    return tg_arn

def create_listener(alb_arn, tg_arn):
    listener = elbv2.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol="HTTP",
        Port=80,
        DefaultActions=[{"Type": "forward", "TargetGroupArn": tg_arn}]
    )
    print("✅ Listener Created")
    return listener

if __name__ == "__main__":
    alb_arn = create_alb()
    
    tg_frontend = create_target_group("tg-frontend-service-v3", 3000)
    tg_hello = create_target_group("tg-hello-service-v3", 7201)
    tg_profile = create_target_group("tg-profile-service-v3", 7202)

    # Attach listeners (for simplicity, frontend default)
    create_listener(alb_arn, tg_frontend)

    print("👉 Now manually add path-based routing in AWS Console:")
    print("   /api/hello → tg-hello-service")
    print("   /api/profile → tg-profile-service")
    print("   / → tg-frontend-service")
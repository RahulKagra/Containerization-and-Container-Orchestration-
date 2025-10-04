import boto3

region = "us-west-2"
ec2 = boto3.client("ec2", region_name=region)
autoscaling = boto3.client("autoscaling", region_name=region)

asg_names = ["jigar-profile-asg", "jigar-hello-asg", "jigar-frontend-asg"]
lt_names  = ["jigar-profile-lt", "jigar-hello-lt", "jigar-frontend-lt"]

# Delete Auto Scaling Groups
for asg in asg_names:
    try:
        autoscaling.delete_auto_scaling_group(
            AutoScalingGroupName=asg,
            ForceDelete=True
        )
        print(f"[+] Deleted ASG: {asg}")
    except Exception as e:
        print(f"[-] Could not delete ASG {asg}: {e}")

# Delete Launch Templates
for lt in lt_names:
    try:
        ec2.delete_launch_template(LaunchTemplateName=lt)
        print(f"[+] Deleted LT: {lt}")
    except Exception as e:
        print(f"[-] Could not delete LT {lt}: {e}")

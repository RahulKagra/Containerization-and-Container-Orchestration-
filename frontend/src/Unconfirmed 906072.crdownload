import boto3

# ---------- CONFIG ----------
REGION = "us-west-2"
VPC_CIDR = "10.0.0.0/16"
SUBNET_CIDR_1 = "10.0.1.0/24"
SUBNET_CIDR_2 = "10.0.2.0/24"

ec2 = boto3.client('ec2', region_name=REGION)

# ---------- CREATE VPC ----------
print("Creating VPC...")
vpc = ec2.create_vpc(CidrBlock=VPC_CIDR)
vpc_id = vpc['Vpc']['VpcId']
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
print(f"✅ VPC created: {vpc_id}")

# ---------- CREATE SUBNETS ----------
print("Creating Subnet 1...")
subnet1 = ec2.create_subnet(CidrBlock=SUBNET_CIDR_1, VpcId=vpc_id, AvailabilityZone=f"{REGION}a")
subnet1_id = subnet1['Subnet']['SubnetId']
print(f"✅ Subnet1: {subnet1_id}")

print("Creating Subnet 2...")
subnet2 = ec2.create_subnet(CidrBlock=SUBNET_CIDR_2, VpcId=vpc_id, AvailabilityZone=f"{REGION}b")
subnet2_id = subnet2['Subnet']['SubnetId']
print(f"✅ Subnet2: {subnet2_id}")

# ---------- INTERNET GATEWAY ----------
print("Attaching Internet Gateway...")
igw = ec2.create_internet_gateway()
igw_id = igw['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
print(f"✅ Internet Gateway: {igw_id}")

# ---------- ROUTE TABLE ----------
print("Creating Route Table...")
route_table = ec2.create_route_table(VpcId=vpc_id)
rt_id = route_table['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=igw_id)
ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet1_id)
ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet2_id)
print(f"✅ Route Table: {rt_id}")

# ---------- SECURITY GROUP ----------
print("Creating Security Group...")
sg = ec2.create_security_group(
    GroupName="mern-sg",
    Description="Security group for MERN app",
    VpcId=vpc_id
)
sg_id = sg['GroupId']

# Allow SSH, HTTP, and custom ports
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 3000, "ToPort": 3002, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 8080, "ToPort": 8080, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
    ]
)
print(f"✅ Security Group created: {sg_id}")

print("🎉 Infrastructure setup complete!")

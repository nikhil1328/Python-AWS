### Friday June 05 17:48 IST 2020
## Purpose ## Python script to launch an EC2 instance with VPC components ##
## Created by Nikhil Kulkarni ##
#########################################################################
# Assuming that you have already configured AWS CLI.

import boto3
ec2 = boto3.resource('ec2')

# create VPC
vpc = ec2.create_vpc(CidrBlock='10.10.0.0/16')
# assign a name to our VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": "python_vpc"}])
vpc.wait_until_available()
# enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )


################### Internet Gateway #######################
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)


################### Subnet #######################
# create subnet and associate it with route table
subnet = ec2.create_subnet(CidrBlock='10.10.10.0/24', VpcId=vpc.id, Availability_Zone='ap-south-1a')
subnet.create_tags(Tags=[{"Key": "Name", "Value": "python_subnet"}])


################### Route Table #######################
# create a route table and a public route
routetable = vpc.create_route_table()
routetable.associate_with_subnet(SubnetId=subnet.id)
routetable.create_tags(Tags=[{"Key": "Name", "Value": "Python_RTB"}])
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

############### Security Group ################
# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='Python_SG', Description='Python_SG', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
securitygroup.create_tags(Tags=[{"Key": "Name", "Value": "Python_SG"}])


################### AWS Key ############
ec2 = boto3.resource('ec2')
# create a file to store the key locally
outfile = open('newkey.pem', 'w')
# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='newkey')
# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)

#################### EC2 #####################

# Create a linux instance in the subnet
instances = ec2.create_instances(
 ImageId='ami-0447a12f28fddb066',
 InstanceType='t2.micro',
 MaxCount=1,
 MinCount=1,
 NetworkInterfaces=[{
 'SubnetId': subnet.id,
 'DeviceIndex': 0,
 'AssociatePublicIpAddress': True,
 'Groups': [securitygroup.group_id]
 }],
 KeyName='key-file-name')

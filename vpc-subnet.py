### Friday June 05 17:17:18 IST 2020
## Purpose ## Python script to create a VPC ##
## Created by Nikhil Kulkarni ##
#########################################################################
# Assuming that you have already configured AWS CLI

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
subnet = ec2.create_subnet(CidrBlock='10.10.10.0/24', VpcId=vpc.id)
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

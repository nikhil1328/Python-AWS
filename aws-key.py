### Friday June 05 16:50:32 IST 2020
## Purpose ## Python script to Create and Download the ec2 .pem file. (AWS Key file for EC2) ##
## Created by Nikhil Kulkarni ##
#########################################################################

import boto3
ec2 = boto3.resource('ec2')

# create a file to store the key locally
outfile = open('mykey.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='mykey')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)

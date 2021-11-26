from src.ec2.vpc import VPC
from src.client_locator import EC2_Client
from src.ec2.ec2 import EC2

def main():

    # instantiate boto3 ec2 resource
    ec2_client = EC2_Client().get_client()

    # create vpc
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc("10.0.0.0/16")
    print(f'VPC created : {vpc_response}')
    print(f"VPC Id : {vpc_response['Vpc']['VpcId']}")

    # add name/resource by using tag
    vpc_name = 'vpc1'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    print(f"add name tag {vpc_name} to {vpc_id}")

    # create internet gateway
    igw_response = vpc.create_igw()
    print(f'IGW created : {igw_response}')
    print(f"IGW Id : {igw_response['InternetGateway']['InternetGatewayId']}")

    # attach internet gateway to vpc
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    vpc.attach_igw_to_vpc(vpc_id, igw_id)
    print(f"internet gateway {igw_id} attached to vpc {vpc_name} with id {vpc_id}")

    # create public subnet
    subnet_response = vpc.create_subnet("10.0.1.0/24", vpc_id)
    print(f'Public Subnet created : {subnet_response}')
    print(f"Public Subnet Id : {subnet_response['Subnet']['SubnetId']}")

    # add name tag to public subnet
    subnet_name = 'PublicSubnet1'
    subnet_id = subnet_response['Subnet']['SubnetId']
    vpc.add_name_tag(subnet_id, subnet_name)

    # create public route table
    rt_response = vpc.create_public_route_table(vpc_id)
    print(f"Route table created : {rt_response}")
    print(f"Public Route Table Id : {rt_response['RouteTable']['RouteTableId']}")

    # create internet gateway route to public route table
    rt_id = rt_response['RouteTable']['RouteTableId']
    vpc.create_igw_route_to_public_route_table(igw_id, rt_id)

    # associate subnet with route table
    vpc.associate_subnet_with_route_table(rt_id, subnet_id)

    # allow auto assign ip address to resources in public subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(subnet_id)

    # create private subnet
    private_subnet_response = vpc.create_subnet("10.0.2.0/24", vpc_id)
    print(f'Private Subnet created : {private_subnet_response}')
    print(f"Private Subnet Id : {private_subnet_response['Subnet']['SubnetId']}")

    # add name tag to private subnet
    private_subnet_name = 'PrivateSubnet1'
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    vpc.add_name_tag(private_subnet_id, private_subnet_name)

    # EC2 instance

    # create ec2 instance
    ec2 = EC2(ec2_client)

    # create key-pair
    key_pair_name = 'key_pair1'
    key_pair_response = ec2.create_key_pair(key_pair_name)
    print(f"Key Pair created : {key_pair_response}")

    # create public security group
    sg_description = "Public security group for public subnet internet access"
    sg_name = "public_sg1"
    sg_response = ec2.create_security_group(sg_description, sg_name, vpc_id)
    print(f"Public Security Group created : {sg_response}")
    print(f"Public Security Group ID : {sg_response['GroupId']}")

    # adding inbound rule to public security group
    sg_id = sg_response['GroupId']
    ec2.add_inbound_rule_to_sg(sg_id)
    print(f"Added public access inbound rule to security group {sg_name} ")

    # create startup script for ec2 instance
    """using bash shell indicating with !/bin/nash
    quick update machine with yum package manager coming from ami
    install httpd24 library from yum repository
    start httpd server on our ec2 instance
    check config for httpd if it is on or not
    after check httpd server, then echoed html file content to a file /var/www/html/index.html"""

    user_data = """#!/bin/bash
                yum update -y
                yum install httpd24 -y
                service httpd start
                chkconfig httpd on
                echo "<html><body><h1> Hello from <b>Sid</b> working on Iaas from Boto3 Python!</h1></body></html>"
                 > /var/www/html/index.html"""

    # Launching an ec2 instance within our public subnet
    # from latest free tier ami image id
    ami_img_id = "ami-041d6256ed0f2061c"
    ec2_instance_type = 't2.micro'
    max_count = 1
    min_count = 1
    ec2.launch_ec2_instance(ami_img_id, ec2_instance_type, key_pair_name, max_count, min_count, sg_id, subnet_id,
                            user_data)
    print(f"Launching Public EC2 instance using ami {ami_img_id} have type {ec2_instance_type}")

    # create private security group for private ec2 instances
    private_sg_description = "Private security group for private subnet"
    private_sg_name = "private_sg1"
    private_sg_response = ec2.create_security_group(private_sg_description, private_sg_name, vpc_id)
    print(f"Private Security Group created : {private_sg_response}")
    print(f"Private Security Group ID : {private_sg_response['GroupId']}")

    # adding inbound rule to private security group
    private_sg_id = private_sg_response['GroupId']
    ec2.add_inbound_rule_to_sg(private_sg_id)
    print(f"Added access inbound rule to security group {sg_name} ")

    # Launching an ec2 instance within our public subnet
    ec2.launch_ec2_instance(ami_img_id, ec2_instance_type, key_pair_name, max_count, min_count, private_sg_id,
                            private_subnet_id, """""")
    print(f"Launching Private EC2 instance using ami {ami_img_id} have type {ec2_instance_type}")

# Describe ec2 instances
def describe_EC2_instances():
    # instantiate boto3 ec2 resource
    ec2_client = EC2_Client().get_client()
    # create ec2 instance
    ec2 = EC2(ec2_client)

    print("Describing EC2 instances")
    ec2_response = ec2.ec2_instances()
    print(str(ec2_response))

# Modifying ec2 instances
def modify_EC2_instances():
        # instantiate boto3 ec2 resource
        ec2_client = EC2_Client().get_client()
        # create ec2 instance
        ec2 = EC2(ec2_client)

        print("Modifying EC2 instances")
        instance_id = "i-04f0c069c72d805df"
        ec2.modify_ec2_instances(instance_id)

# Stop ec2 instances
def stop_EC2_instances():
        # instantiate boto3 ec2 resource
        ec2_client = EC2_Client().get_client()
        # create ec2 instance
        ec2 = EC2(ec2_client)

        print("Stop EC2 instances")
        instance_id = "i-0cf9276ec50c300fe"
        ec2.stop_ec2_instances(instance_id)

# Start ec2 instances
def start_EC2_instances():
    # instantiate boto3 ec2 resource
    ec2_client = EC2_Client().get_client()
    # create ec2 instance
    ec2 = EC2(ec2_client)

    print("Start EC2 instances")
    instance_id = "i-0cf9276ec50c300fe"
    ec2.start_ec2_instances(instance_id)

# Shut-down ec2 instances
def terimnate_EC2_instances():
    ec2_client = EC2_Client().get_client()
    ec2 = EC2(ec2_client)

    print("Shutdown EC2 instances")
    instance_id = "i-04f0c069c72d805df"
    ec2.terminate_ec2_instances(instance_id)


if __name__ == '__main__':
    # main()
    # describe_EC2_instances()
    modify_EC2_instances()
    # stop_EC2_instances()
    # start_EC2_instances()
    terimnate_EC2_instances()
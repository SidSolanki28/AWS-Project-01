import boto3

class EC2:

    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    # create key-pair
    def create_key_pair(self, key_name):
        return self._client.create_key_pair(KeyName=key_name)

    # create security group
    def create_security_group(self, sg_description, sg_name, vpc_id):
        return self._client.create_security_group(
            Description=sg_description,
            GroupName=sg_name,
            VpcId=vpc_id
        )

    # adding inbound rule to security group
    def add_inbound_rule_to_sg(self, sg_id):
        return self._client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

    # Launching an ec2 instance within our public subnet
    def launch_ec2_instance(self, image_id, instance_type, key_name, max_count, min_count, sg_id, subnet_id, user_data):
        return self._client.run_instances(ImageId=image_id,
                                          InstanceType=instance_type,
                                          KeyName=key_name,
                                          MaxCount=max_count,
                                          MinCount=min_count,
                                          SecurityGroupIds=[sg_id],
                                          SubnetId=subnet_id,
                                          UserData=user_data
                                          )

    # Describe ec2 instances
    def describe_ec2_instances(self):
        return self._client.describe_instances()

    # Modifying ec2 instances
    def modify_ec2_instances(self, instance_id):
        return self._client.modify_instance_attribute(
            DisableApiTermination={'Value': False},
            InstanceId=instance_id
        )

    # Stop ec2 instances
    def stop_ec2_instances(self, instance_id):
        return self._client.stop_instances(
            InstanceIds=[instance_id]
        )

    # Start ec2 instances
    def start_ec2_instances(self, instance_id):
        return self._client.start_instances(
            InstanceIds=[instance_id]
        )

    # Shutdown ec2 instances
    def terminate_ec2_instances(self, instance_id):
        return self._client.terminate_instances(
            InstanceIds=[instance_id]
        )








import boto3

class VPC:

    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2 """

    # create vpc
    def create_vpc(self, ip_cidr):
        vpc = self._client.create_vpc(CidrBlock=ip_cidr)
        return vpc

    # add name/resource by using tag
    def add_name_tag(self, resource_id, resource_name):
        self._client.create_tags(
            Resources=[resource_id],
            Tags=[{"Key": "Name", "Value": resource_name}]
        )
        return

    # create internet gateway
    def create_igw(self):
        return self._client.create_internet_gateway()

    # attach internet gateway to vpc
    def attach_igw_to_vpc(self, vpc_id, igw_id):
        self._client.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    # create_subnet
    def create_subnet(self, ip_cidr, vpc_id):
        subnet = self._client.create_subnet(
            CidrBlock=ip_cidr,
            VpcId=vpc_id
        )
        return subnet

    # create public route table
    def create_public_route_table(self, vpc_id):
        route_table = self._client.create_route_table(VpcId=vpc_id)
        return route_table

    # create internet gateway route to public route table
    def create_igw_route_to_public_route_table(self, igw_id, rt_id):
        route = self._client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=igw_id,
            RouteTableId=rt_id
        )
        return route

    # associate subnet with route table
    def associate_subnet_with_route_table(self, rt_id, subnet_id):
        return self._client.associate_route_table(
            RouteTableId=rt_id,
            SubnetId=subnet_id
        )

    # allow auto assign ip address to resources in public subnet
    def allow_auto_assign_ip_addresses_for_subnet(self, subnet_id):
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )


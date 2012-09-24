import boto.ec2
from boto.ec2 import autoscale, elb
from cloud import models


class AWSConnectionHandler:
    """
    Class managing shared AWS connections
    """
    # AWS EC2 connection
    as_connections = {}
    ec2_connections = {}
    elb_connections = {}

    def connect_to_as(self, cloud_id):
        """
        Connect to AWS AS
        """
        cloud = models.Cloud.objects.get(uuid=cloud_id)
        self.as_connections[cloud_id] = autoscale.connect_to_region(
            cloud.region,
            aws_access_key_id=cloud.aws_access_key,
            aws_secret_access_key=cloud.aws_secret_key)

    def connect_to_ec2(self, cloud_id):
        """
        Connect to AWS EC2
        """
        cloud = models.Cloud.objects.get(uuid=cloud_id)
        self.ec2_connections[cloud_id] = boto.ec2.connect_to_region(
            cloud.region,
            aws_access_key_id=cloud.aws_access_key,
            aws_secret_access_key=cloud.aws_secret_key)

    def connect_to_elb(self, cloud_id):
        """
        Connect to AWS ELB
        """
        cloud = models.Cloud.objects.get(uuid=cloud_id)
        self.elb_connections[cloud_id] = elb.connect_to_region(
            cloud.region,
            aws_access_key_id=cloud.aws_access_key,
            aws_secret_access_key=cloud.aws_secret_key)

    def get_as_connection(self, cloud_id):
        """
        Return AS connection
        """
        try:
            self.as_connections[cloud_id]
        except KeyError:
            self.connect_to_as(cloud_id)
        finally:
            return self.as_connections[cloud_id]

    def get_ec2_connection(self, cloud_id):
        """
        Return EC2 connection
        """
        try:
            self.ec2_connections[cloud_id]
        except KeyError:
            self.connect_to_ec2(cloud_id)
        finally:
            return self.ec2_connections[cloud_id]

    def get_elb_connection(self, cloud_id):
        """
        Return ELB connection
        """
        try:
            self.elb_connections[cloud_id]
        except KeyError:
            self.connect_to_elb(cloud_id)
        finally:
            return self.elb_connections[cloud_id]

    def terminate_connections(self, cloud_id):
        """
        Terminate all AWS connections
        """
        self.as_connections.pop(cloud_id)
        self.ec2_connections.pop(cloud_id)
        self.elb_connections.pop(cloud_id)

HANDLER = AWSConnectionHandler()

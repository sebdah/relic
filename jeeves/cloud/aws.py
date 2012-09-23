import boto.ec2
from boto.ec2 import autoscale
from cloud import models


class AWSConnectionHandler:
    """
    Class managing shared AWS connections
    """
    # AWS EC2 connection
    ec2_connections = {}
    as_connections = {}

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

HANDLER = AWSConnectionHandler()

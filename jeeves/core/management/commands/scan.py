"""
Scanning command for updating database according to AWS reality
"""

import sys
from cloud import models, aws
from optparse import make_option
from django.core.management.base import BaseCommand  # CommandError


class Command(BaseCommand):
    args = ''
    help = 'Scan AWS for environment changes'

    option_list = BaseCommand.option_list + (
        make_option('--cloud', action='store',
            dest='cloud', default='',
            help='Monitor this specific cloud'),)

    def handle(self, *args, **options):
        """
        Execution method
        """
        # Get the clouds
        clouds = models.Cloud.objects.all()
        if options.get('cloud') is not '':
            clouds = models.Clouds.objects.filter(uuid=options.get('cloud'))

        for cloud in clouds:
            # Connect to EC2
            as_con = aws.HANDLE.get_as_connection(cloud.uuid)
            ec2_con = aws.HANDLE.get_ec2_connection(cloud.uuid)

            #
            # CHECK 1: Update has_instances flag for ASGDefs
            #
            print "Scanning cloud %s (%s)" % (cloud.name, cloud.uuid)
            for asg_def in models.AutoScalingGroupDefinition.objects.all():
                print " * Scanning ASG %s-%s" % (cloud.name, asg_def.version)
                asg = as_con.get_all_groups(names=['%s-%s' % (
                    cloud.name, asg_def.version)])

                # If the asg_def has no ASG in AWS
                if len(asg) == 0:
                    print " * %s-%s is not registered at AWS" % (
                        cloud.name, asg_def.version)
                    asg_def.is_registered(False)
                    asg_def.has_instances(False)
                    asg_def.save()
                else:
                    # Find out if there are any instances assigned
                    instance_ids = [i.id for i in asg.instances]
                    reservations = ec2_con.get_all_instances(instance_ids)
                    instances = [i for r in reservations for i in r.instances]

                    # Count only running or pending instances
                    running_count = 0
                    for instance in instances:
                        if instance.state_code in [0, 16]:
                            # 0 == Pending
                            # 16 == Running
                            running_count += 1

                    # Update model
                    if running_count > 0:
                        asg_def.has_instances(True)
                        print " * %s-%s has %i running/pending instances" % (
                            cloud.name, asg_def.version, running_count)
                    else:
                        asg_def.has_instances(False)
                        print """\
 * %s-%s is registered but has no running instances""" % (
    cloud.name, asg_def.version, running_count)
                    asg_def.is_registered(True)
                    asg_def.save()

        sys.exit(0)

import boto3
from scheduler.campaigns import CampaignsScheduler
from scheduler.tools import Tools


class InstancesLauncher:

    def __init__(self):
        self.ami = 'ami-09cb3b7efa60fd48a'
        self.ec2 = boto3.resource('ec2')

    def launch_instance(self, bot):
        self.ec2.create_instances(
            ImageId='{0}'.format(self.ami),
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.medium',
            KeyName='dsirf_fb_scrappers',
            SecurityGroupIds=['sg-0e56e0381b8f8cfb4'],
            SubnetId='subnet-c082b8ba',
            UserData="{0}".format(bot)
        )

    def terminate_instance(self, instance_id):
        self.ec2.instances.filter(InstanceIds=[instance_id]).terminate()

    def describe_instances(self):
        return self.ec2.instances.filter(Filters=[{
                                        'Name': 'instance-state-name',
                                        'Values': ['running']},
                                        {'Name': 'image-id',
                                        'Values': [self.ami]}])

# db = Tools(InstancesLauncher())
# db.tools()

# db = CampaignsScheduler(InstancesLauncher())
# db.campaigns()

import boto3
from setting import ami, security_group_ids, key_name, instance_type

ec2 = boto3.client('ec2')

machine_list = []

def deploy_script(type):
    deploy = None
    if type == 'worker':
        deploy = """#!/bin/bash
        git clone https://github.com/noam-stein/dsp_Assignment_1.git
        ipython ./dsp_Assignment_1/workers/worker.py"""
    elif type == 'manager':
        deploy = """#!/bin/bash
              git clone https://github.com/noam-stein/dsp_Assignment_1.git
              ipython ./dsp_Assignment_1/manager/manager.py"""
    return deploy


def create_instances(type, number_of_instances):
    script = deploy_script(type)
    instance = ec2.create_instances(
        ImageId=ami,
        MinCount=number_of_instances,
        MaxCount=number_of_instances,
        UserData=script,
        SecurityGroupIds=security_group_ids,
        KeyName=key_name,
        InstanceType=instance_type)

    machine_list.extend(instance)



    #
    #
    # """instance = ec2.create_instances(
    #    ...:     ImageId='ami-86825ee9',
    #    ...:     MinCount=1,
    #    ...:     MaxCount=1,
    #    ...:     UserData="""#!/bin/bash
    #    ...:     mkdir -p /home/ubuntu/d/t/s""",
    #    ...:     SecurityGroupIds=["sg-becc70d5"],
    #    ...:     KeyName="MyKeyPair",
    #    ...:     InstanceType='t2.micro')"""
    #
    # """ instance = ec2.create_instances(
    #     ...:     ImageId='ami-e4c63e8b',
    #     ...:     MinCount=1,
    #     ...:     MaxCount=1,
    #     ...:     UserData="#!/bin/bash \n mkdir \"
    #     ...: hwllo word\"",
    #     ...:     KeyName="MyKeyPair",
    #     ...:  InstanceType='t2.micro')"""
    #
    # "ami-86825ee9"
    # """instance = ec2.create_instances(
    #     ...:     ImageId='ami-e4c63e8b',
    #     ...:     MinCount=1,
    #     ...:     MaxCount=1,
    #     ...:     SecurityGroupIds=["sg-becc70d5"],
    #     ...:
    #     ...:     KeyName="MyKeyPair",
    #     ...:     InstanceType='t2.micro')"""
    #
    #
    # """"nstance = ec2.create_instances(
    #    ...:     ImageId='ami-86825ee9',
    #    ...:     MinCount=1,
    #    ...:     MaxCount=1,
    #    ...:     UserData="#!/bin/bash  mkdir -p ~/t/d/s",
    #    ...:     SecurityGroupIds=["sg-becc70d5"],
    #    ...:     KeyName="MyKeyPair",
    #    ...:     InstanceType='t2.micro')"""

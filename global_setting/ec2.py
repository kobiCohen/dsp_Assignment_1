import boto3
from setting import ami, security_group_ids, key_name, instance_type

ec2 = boto3.resource('ec2')

worker_machine_list = []
manger_machine = []


def deploy_script(machine_type):
    """     
    return the script for deploy 
    :param instances_type: string worker|manager
    :return: a string for deploy worker|manager in the machine
    """
    deploy = None
    if machine_type == 'worker':
        deploy = """#!/bin/bash
        runuser -l ubuntu -c 'cd /home/ubuntu ;git clone https://github.com/noam-stein/dsp_Assignment_1.git'
        runuser -l ubuntu -c 'cd /home/ubuntu/dsp_Assignment_1; python ./workers/worker.py &> /home/ubuntu/log.txt' 
        """
    elif machine_type == 'manager':
        deploy = """#!/bin/bash \n
        runuser -l ubuntu -c 'cd /home/ubuntu ;git clone https://github.com/noam-stein/dsp_Assignment_1.git'
        runuser -l ubuntu -c 'cd /home/ubuntu/dsp_Assignment_1; python ./manager/manager.py &> /home/ubuntu/log.txt' 
        """
    return deploy


def create_instances(machine_type, number_of_instances):
    """
    create new ec2  machine for worker|manager and deploy it
    :param machine_type: string worker|manager
    :param number_of_instances: how many machine create
    :return: None
    """

    if number_of_instances > len(worker_machine_list):
        number_of_instances = number_of_instances - len(worker_machine_list)


    #TODO: need to inc the number of instances until then hack
    if number_of_instances + len(worker_machine_list) + 1 >= 10 and machine_type == 'worker':
        number_of_instances = 10 - (len(worker_machine_list) + 1)

    script = deploy_script(machine_type)
    instance = ec2.create_instances(
        ImageId=ami,
        MinCount=number_of_instances,
        MaxCount=number_of_instances,
        UserData=script,
        SecurityGroupIds=security_group_ids,
        KeyName=key_name,
        InstanceType=instance_type,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': machine_type,
                        'Value': machine_type
                    }
                ]
            }
        ]
    )
    if machine_type == 'worker':
        worker_machine_list.extend(instance)
    else:
        manger_machine.extend(instance)


def delete_all_instances():
    """
    terminate all ec2 instances
    :return: None
    """
    for machine in worker_machine_list:
        machine.terminate()
    manger_machine[0].terminate()


def delete_all_workers():
    """
    terminate all worker instances
    :return: None
    """
    for machine in worker_machine_list:
        machine.terminate()


def get_number_of_worker():
    """
    get how many worker are running 
    :return: number  
    """
    return len(worker_machine_list)


if __name__ == '__main__':
    create_instances('worker', 1)
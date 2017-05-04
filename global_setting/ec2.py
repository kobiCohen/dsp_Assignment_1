import boto3
from setting import ami, security_group_ids, key_name, instance_type

ec2 = boto3.resource('ec2')


def deploy_script(machine_type):
    """     
    return the script for deploy 
    :param instances_type: string -> worker|manager
    :return: string -> string for deploy worker|manager in the machine
    """
    if machine_type == 'worker':
        return """#!/bin/bash
        runuser -l ubuntu -c 'cd /home/ubuntu ;git clone https://github.com/noam-stein/dsp_Assignment_1.git'
        runuser -l ubuntu -c 'cd /home/ubuntu/dsp_Assignment_1; python ./workers/worker.py &> /home/ubuntu/log.txt' 
        """
    elif machine_type == 'manager':
        return """#!/bin/bash \n
        runuser -l ubuntu -c 'cd /home/ubuntu ;git clone https://github.com/noam-stein/dsp_Assignment_1.git'
        runuser -l ubuntu -c 'cd /home/ubuntu/dsp_Assignment_1; python ./manager/manager.py &> /home/ubuntu/log.txt' 
        """


def create_instances(machine_type, number_of_instances=1):
    """
    create new ec2  machine for worker|manager and deploy it
    :param machine_type: string -> worker|manager
    :param number_of_instances: int -> how many machine create
    :return: None
    """
    number_of_workers = get_number_of_worker()
    if number_of_instances > number_of_workers:
        number_of_instances = number_of_instances - number_of_workers
    else:
        return None

    script = deploy_script(machine_type)
    ec2.create_instances(
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


def delete_all_workers():
    """
    terminate all worker instances
    :return: None
    """
    for machine in get_workers():
        machine.terminate()


def delete_the_manager():
    """
    terminate the manager
    :return:None 
    """
    manger = get_manager()
    if manger is not None:
        manger.terminate()


def get_number_of_worker():
    """
    get how many worker are running 
    :return: int -> number  
    """
    return len(get_workers())


def get_workers():
    """
    get all the worker that running or going to run
    :returns list -> list of all the worker instances
    """
    list_of_workers = []
    for instance in ec2.instances.all():
        if instance.state[u'Name'] == 'pending' or instance.state[u'Name'] == 'running':
            for tag in instance.tags:
                if tag[u'Key'] == 'worker':
                    list_of_workers.append(instance)
    return list_of_workers


def get_manager():
    """
    get the manger
    :returns None or the manager
    """
    for instance in ec2.instances.all():
        if instance.state[u'Name'] == 'pending' or instance.state[u'Name'] == 'running':
            for tag in instance.tags:
                if tag[u'Key'] == 'manager':
                    return instance
    return None

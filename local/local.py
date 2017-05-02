import sys
import os
import uuid
import json
cwd = os.getcwd()
sys.path.append(cwd)
import boto3

import global_setting.s3 as s3
import global_setting.sqs as sqs
import global_setting.ec2 as ec
from global_setting.setting import download_pdf_dic

local_id = uuid.uuid4()


ec2 = boto3.resource('ec2')

worker_machine_list = []
manger_machine = []




def get_manager():
    """
    checks currnet machines to see if a manager exists
    :returns a machine that's a manager
    """
    ec2 = boto3.resource('ec2')
    manager = None
#    for instance in filter(lambda inst: len(inst.tags) > 0, ec2.instances.all()):
#        for tag in instance.tags:
#            if tag.get('manager', None) == 'manager':
#                print "Got manager", instance.id
#                manager = instance
    if manager is None:
        ec.create_instances("manager", 1)
        print "create"
    return manager


def send_start_message(loc):
    """
    Sends a message to the manager's queue for starting
    """
    txt_loc = loc
    task_id = "40"
    terminate = False
    number_of_workers = 3

    message = json.dumps([txt_loc, task_id, terminate, number_of_workers])
    #print "message sent", message
    sqs.new_task.send_message(MessageBody=message)


def wait_to_end():
    # type: () -> object
    """
    Waits till the manager sends a job is done message
    :return: results of processing the file
    """

    res = None
    while True:
        res = sqs.done_task.receive_messages(1)
        if res:
            break
    print "Got message"
    print res
    return res


def process_res():
    pass


def local_main():
    """
    starts thr actions of the local
    checks if a manager computer is on, if is - sends him a message. if not, sends depoloys a new machine
    """
    ec.create_instances("manager", 1)
    args = sys.argv

    local_file_loc = args[1]
    open(local_file_loc, 'rb')
    s3.upload_file(local_file_loc, download_pdf_dic)
    send_start_message(download_pdf_dic)
    res = wait_to_end()
    print res
    process_res(res)


if __name__ == "__main__":
    local_main()




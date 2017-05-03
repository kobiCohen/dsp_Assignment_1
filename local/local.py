import sys
import os
import uuid
import json

cwd = os.getcwd()
sys.path.append(cwd)
import boto3
import end
import global_setting.s3 as s3
import global_setting.sqs as sqs
import argparse
import tarfile
from global_setting.ec2 import get_manager, create_instances
from global_setting.setting import download_pdf_dic, bucket_name
from time import sleep

local_id = str(uuid.uuid4())

worker_machine_list = []
manger_machine = []


def send_start_message(task_name, number_of_worker, terminate):
    task_id = local_id
    terminate = terminate
    number_of_workers = number_of_worker

    message = json.dumps([task_name, task_id, terminate, number_of_workers])
    sqs.new_task.send_message(MessageBody=message)


def wait_to_end():
    """
    Waits till the manager sends a job is done message
    :return: results of processing the file
    """
    while True:
        res = sqs.get_sqs_queue(local_id).receive_messages(1)
        if res:
            return res[0]
        sleep(1)

def download_file_and_create_link(pdf_loc_in_s3, task_type):
    task_folder = '{}/{}/'.format(cwd, task_type)
    local_file_loc = '{}temp.tar.gz '.format(task_folder)
    s3.download_file(pdf_loc_in_s3, local_file_loc)
    with tarfile.open(local_file_loc) as tar:
        tar.extractall(task_folder)
    os.remove(local_file_loc)



def process_res(res):
    result_string = res.body
    returned_results = json.loads(result_string)
    links = []
    for task_type, pdf_loc_in_s3, task_url, task_group_id, successfully in returned_results:
        if successfully is True:
            links.append(download_file_and_create_link(pdf_loc_in_s3, task_type))

    end.create_site(links)


def local_main(file_loc, number_of_worker, terminate):
    """
    starts thr actions of the local
    checks if a manager computer is on, if is - sends him a message. if not, sends depoloys a new machine
    """
    # check if the manager is alive if not create one
    if get_manager():
        create_instances('manager')
    task_name = '{}_task.txt'.format(local_id)
    s3.upload_file(file_loc, task_name)
    send_start_message(task_name, number_of_worker, terminate)
    res = wait_to_end()
    process_res(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='for local')
    parser.add_argument('-f', action="store", type=str, dest='file')
    parser.add_argument('-n', action="store", type=int, dest='number')
    parser.add_argument('-t', action="store_true", default=False, dest='terminate')
    args = parser.parse_args()
    file_loc = args.file
    number_of_worker = args.number
    terminate = args.terminate
    local_main(file_loc, number_of_worker, terminate)

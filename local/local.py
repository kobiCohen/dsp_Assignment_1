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
from os.path import join
from simple_web import  build_and_run_server
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


def download_file_and_create_link(pdf_loc_in_s3, task_type, work_dir):

    task_folder = '{}/{}/'.format(work_dir, task_type)
    local_file_loc = '{}temp.tar.gz '.format(task_folder)
    s3.download_file(pdf_loc_in_s3, local_file_loc)
    with tarfile.open(local_file_loc) as tar:
        tar.extractall(task_folder)
    os.remove(local_file_loc)


def get_pdf_loc_in_local(pdf_name, task_type):
    local_loc = '{}/{}/{}'.format(cwd, task_type, pdf_name)
    if task_type == 'ToImage':
        return '{}.png'.format(local_loc)
    elif task_type == 'ToHTML':
        return '{}.html'.format(local_loc)
    elif task_type == 'ToText':
        return '{}.txt'.format(local_loc)


def process_res(res):
    work_dir = join(cwd, local_id)
    os.mkdir(work_dir)
    os.mkdir(join(cwd, local_id, 'ToImage'))
    os.mkdir(join(cwd, local_id, 'ToHTML'))
    os.mkdir(join(cwd, local_id, 'ToText'))
    result_string = res.body
    res.delete()
    returned_results = json.loads(result_string)
    link_list = []
    for task_type, pdf_loc_in_s3, task_url, task_group_id, successfully in returned_results:
        if successfully is True:
            # get the file name from the pdf url in s3
            pdf_name = pdf_loc_in_s3.split('/')[-1].split('.')[0]
            download_file_and_create_link(pdf_loc_in_s3, task_type, work_dir)
            # add the local loc file to the list
            link_list.append(get_pdf_loc_in_local(pdf_name, task_type))
    return work_dir


def local_main(file_loc, number_of_worker, terminate, port):
    """
    starts thr actions of the local
    checks if a manager computer is on, if is - sends him a message. if not, sends depoloys a new machine
    """
    # check if the manager is alive if not create one
    if get_manager() is None:
        create_instances('manager')
    task_name = '{}_task.txt'.format(local_id)
    s3.upload_file(file_loc, task_name)
    send_start_message(task_name, number_of_worker, terminate)
    res = wait_to_end()
    web_home_server_dic = process_res(res)
    build_and_run_server(web_home_server_dic, port)

def main():
    parser = argparse.ArgumentParser(description='for local')
    parser.add_argument('-f', action="store", type=str, dest='file')
    parser.add_argument('-n', action="store", type=int, dest='number')
    parser.add_argument('-t', action="store_true", default=False, dest='terminate')
    parser.add_argument('-p', action="store", default=5007, dest='port')
    args = parser.parse_args()
    file_loc = args.file
    number_of_worker = args.number
    terminate = args.terminate
    port = args.port
    local_main(file_loc, number_of_worker, terminate, port)


if __name__ == "__main__":
    main()
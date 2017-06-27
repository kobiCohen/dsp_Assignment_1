from colorlog import ColoredFormatter
import sys
import os
import uuid
import json
cwd = os.getcwd()
sys.path.append(cwd)
import boto3

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
import logging


log = logging.getLogger('local')


def build_logger():
    """
    build the logger
    :return: None 
    """
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    color_formatter = ColoredFormatter("%(log_color)s - %(levelname)s - %(message)s%(reset)s")
    ch.setFormatter(color_formatter)
    log.addHandler(ch)


def send_start_message(task_loc_in_s3_name, number_of_worker, terminate):
    """
    create a task sqs for the manager and send it
    :param task_loc_in_s3_name: string ->  where you can find the task in s3
    :param number_of_worker:  int -> number of worker
    :param terminate:  bool -> should terminate
    :return: None
    """
    task_id = local_id
    terminate = terminate
    number_of_workers = number_of_worker

    message = json.dumps([task_loc_in_s3_name, task_id, terminate, number_of_workers])
    sqs.new_task.send_message(MessageBody=message)


def wait_to_end():
    """
    busy wait till the manager sends a job is done message
    :return: sqs message obj
    """
    while True:
        res = sqs.get_sqs_queue(local_id).receive_messages(1)
        if res:
            return res[0]
        sleep(1)


def download_file_and_create_link(pdf_loc_in_s3, task_type, work_dir):
    """
    download the file from s3 untar it and remove the tar
    :param pdf_loc_in_s3: string -> the loc in s3
    :param task_type:  string -> task type
    :param work_dir:  string -> working dir
    :return: None
    """
    task_folder = '{}/{}/'.format(work_dir, task_type)
    local_file_loc = '{}temp.tar.gz '.format(task_folder)
    s3.download_file(pdf_loc_in_s3, local_file_loc)
    with tarfile.open(local_file_loc) as tar:
        tar.extractall(task_folder)
    os.remove(local_file_loc)


def get_pdf_loc_in_local(pdf_name, task_type):
    """
    get the loc of the file in your local pc
    :param pdf_name: string -> the pdf namme
    :param task_type: string -> the task file
    :return: string -> the full path of the local convert file
    """
    local_loc = '{}/{}/{}'.format(cwd, task_type, pdf_name)
    if task_type == 'ToImage':
        return '{}.png'.format(local_loc)
    elif task_type == 'ToHTML':
        return '{}.html'.format(local_loc)
    elif task_type == 'ToText':
        return '{}.txt'.format(local_loc)


def create_local_folder(work_dir):
    """
    create the local folder
    :param work_dir: string -> the working dic
    :return: None 
    """
    os.mkdir(work_dir)
    os.mkdir(join(cwd, local_id, 'ToImage'))
    os.mkdir(join(cwd, local_id, 'ToHTML'))
    os.mkdir(join(cwd, local_id, 'ToText'))


def process_res(res):
    """
    process the result from the manager
    :param res:  string-> the summery report
    :return: string -> the working dir
    """
    work_dir = join(cwd, local_id)
    create_local_folder(work_dir)
    result_string = res.body
    res.delete()
    returned_results = json.loads(result_string)
    link_list = []
    error_report = ""
    for task_type, pdf_loc_in_s3, task_url, task_group_id, successfully, resone_failed in returned_results:
        if successfully is True:
            # get the file name from the pdf url in s3
            pdf_name = pdf_loc_in_s3.split('/')[-1].split('.')[0]
            download_file_and_create_link(pdf_loc_in_s3, task_type, work_dir)
            # add the local loc file to the list
            link_list.append(get_pdf_loc_in_local(pdf_name, task_type))
        else:
            error_message = 'task_type: {}  pdf_ur: {}  why: {} \n'.format(task_type, task_url, resone_failed)
            logging.warning(error_message)
            error_report += error_message
    with open(join(work_dir, 'error_report.txt'), 'w+') as txt_file:
        txt_file.write(error_report)
    return work_dir


def local_main(file_loc, number_of_worker, terminate, port):
    """
    the local main
    :param file_loc: string -> the task file loc 
    :param number_of_worker:  int -> number of worker per task
    :param terminate:  bool -> should terminate
    :param port: int -> the port of local site
    :return: 
    """
    # check if the manager is alive if not create one
    if get_manager() is None:
        log.info('no manager found, create new manager')
        create_instances('manager')
    else:
        log.info('found a manager no need to create one')
    task_loc_in_s3 = '{}_task.txt'.format(local_id)
    log.info('upload to s3 the file {}'.format(file_loc))
    s3.upload_file(file_loc, task_loc_in_s3)
    log.info('send the start message to the manager')
    send_start_message(task_loc_in_s3, number_of_worker, terminate)
    log.info('going to busy wait for the result')
    res = wait_to_end()
    log.info('manager send done message, going to download the file from s3')
    web_home_server_dic = process_res(res)
    log.info('going to create the web site')
    build_and_run_server(web_home_server_dic, port)


def main():
    """
    thr main parse args from command line
    :return: None
    """
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
    log.info('local start is life')
    log.info('the task id {}'.format(local_id))
    local_main(file_loc, number_of_worker, terminate, port)


if __name__ == "__main__":
    build_logger()
    main()

import json
import os
import sys
import thread

# this is a small hack so the worker will add the working dic to the sys file path
cwd = os.getcwd()
sys.path.append(cwd)

from logger.logger import Logger
from global_setting.sqs import new_task, new_pdf_tasks, done_pdf_tasks
from global_setting.s3 import download_file
from global_setting.ec2 import create_instances, get_number_of_worker, delete_all_workers
from task import Task
from task_collection import TaskCollection

log = Logger('manager')

# this list old all the task_jobs
task_col = TaskCollection()
os.environ['S3_USE_SIGV4'] = 'True'
done_taksk = []
def get_new_message(sqs_queue):
    """
    get one message from the sqs_queue
    and convert it from json to python structure
    :param sqs_queue: sqs queue
    :return: one sqs message and if the queue os empty return None
    """
    message = sqs_queue.receive_messages(1)
    if len(message) > 0:
        return message[0]
    else:
        return None


def send_pdf_tasks_to_workers(pdf_task_list):
    for task in pdf_task_list:
        task_json = json.dumps(task)
        new_pdf_tasks.send_message(MessageBody=task_json)


def create_task_obj(pdf_tasks_list, task_id):
    new_task_obj = Task(pdf_tasks_list, task_id)
    task_col.add_new_task(task_id, new_task_obj)


def get_pdf_tasks(s3_txt_loc, task_id):
    task_list = []
    local_txt_loc = '/tmp/{0}.txt'.format(task_id)
    download_file(s3_txt_loc, local_txt_loc)
    with open(local_txt_loc, 'r') as task_file:
        for line in task_file.readlines():
            job_type, url = line.split('\n')[0].split('\t')
            new_pdf_task = [job_type, url, task_id]
            task_list.append(new_pdf_task)
    return task_list


def start_new_task(terminate):
    task = get_new_message(new_task)

    # enter the if statement only if task is not None
    if task:
        # convert the json to python object
        # the json is in the format [pdf_loc_in_s3, task_id, terminate?, number_of_workers]
        txt_loc, task_id, terminate, number_of_workers = json.loads(task.body)
        pdf_tasks_list = get_pdf_tasks(txt_loc, task_id)
        create_task_obj(pdf_tasks_list, task_id)
        send_pdf_tasks_to_workers(pdf_tasks_list)
        number_of_needed_machine = int(len(pdf_tasks_list) / number_of_workers)
        difference_between_machine = number_of_needed_machine - get_number_of_worker()
        if difference_between_machine > 0:
            create_instances('worker', difference_between_machine)
        task.delete()
    return terminate


def get_all_pdf_task_from_workers():
    while True:
        pdf_task_message = get_new_message(done_pdf_tasks)
        # if the message queue is empty exit
        if pdf_task_message is None:
            break
        try:
            task_type, pdf_loc_in_s3, task_url, task_group_id, successfully = json.loads(pdf_task_message.body)
        except Exception as ex:
            log.exception(ex)
            pdf_task_message.delete()
            return None
        pdf_task_message.delete()
        new_pdf_done_task = [task_type, pdf_loc_in_s3, task_url, task_group_id, successfully]
        task_col.add_new_pdf_task_done(task_group_id, new_pdf_done_task)
        done_taksk.append(new_pdf_done_task.pdf_loc_in_s3)


def get_pdf_message():
    while True:
        get_all_pdf_task_from_workers()
        task_col.check_if_task_done(done_taksk)


def send_message():
    terminate = False
    while True:
        if terminate is False:
            terminate = start_new_task(terminate)
        if terminate is True and task_col.all_task_are_done():
            delete_all_workers()


def main_loop():
    log.info('manager start is life cycle')
    thread.start_new_thread(get_pdf_message, ())
    send_message()
    # get_pdf_message()
    # send_message()


# you will enter the if statement only when the module is main
if __name__ == "__main__":
    try:
        main_loop()
    except Exception as ex:
        log.exception(ex, info='this Exception is main, the manager cant recover \n good but cruel world\n')
        main_loop()

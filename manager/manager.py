import boto3
import json
from logger.logger import Logger
from global_setting.setting import bucket_name

s3 = boto3.resource('s3')

log = Logger('manager')
# this list old all the task_jobs
tasks_jobs_list = []


def get_new_message(sqs_queue):
    """
    get one message from the sqs_queue
    and convert it from json to python structure
    :param sqs_queue: a sqs queue
    :return: one sqs message and if the queue os empty return None
    """
    message = sqs_queue.receive_messages(1)
    if len(message) > 0:
        return message[0]
    else:
        return None


def send_pdf_tasks_to_workers(task_job):
    pass


def create_task_obj(pdf_tasks_list, task_id):
    pass


def get_pdf_tasks(s3_txt_loc, task_id):
    task_list = []
    local_txt_loc = '/tmp/{0}.txt'.format(task_id)
    s3.meta.client.download_file(bucket_name, s3_txt_loc, local_txt_loc)
    with open(local_txt_loc, 'r') as task_file:
        for line in task_file.readlines():
            job_type, url = line.split('\n')[0].split('\t')
            new_pdf_task = [job_type, url, task_id]
            task_list.append(new_pdf_task)
    return task_list


def start_new_task():
    task = get_new_message(new_task)
    terminate = False
    # enter the if statement only if task is not None
    if task:
        # convert the json to python object
        # the json is in the format [pdf_loc_in_s3, task_id, terminate?, number_of_workers]
        txt_loc, task_id, terminate, number_of_workers = json.loads(task.body)
        pdf_tasks_list = get_pdf_tasks(txt_loc, task_id)
        send_pdf_tasks_to_workers(pdf_tasks_list)
        new_task_obj = create_task_obj(pdf_tasks_list, task_id)
        tasks_jobs_list.append(new_task_obj)
        task.delete()
    return terminate


def check_if_task_done():
    pass


def get_all_pdf_task_from_workers():
    pass


def main_loop():
    terminate = False
    while True:
        if terminate is False:
            terminate = start_new_task()
        get_all_pdf_task_from_workers()
        check_if_task_done()
        # if terminate is True and all_task_are_done():
        #     terminate_workers()
        #     terminate_manager()


def manager_main():
    main_loop()


# you will enter the if statement only when the module is main
if __name__ == "__main__":
    manager_main()



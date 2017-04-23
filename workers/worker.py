import boto3
import json

from logger.logger import Logger
from pdf_to_htm import ConvetToHtml
from pdf_to_img import ConvetToImg
from pdf_to_txt import ConvetToTxt

sqs = boto3.resource('sqs')
task_sqs = sqs.create_queue(QueueName='task')
log = Logger()


def implement_task(task):
    task_type = task[0]
    task_url = task[1]
    if task_type == 'ToImage':
        ConvetToHtml(task)
    elif task_type == 'ToHTML':
        ConvetToImg(task)
    elif task_type == 'ToText':
        ConvetToTxt(task)
    else:
        log.warning('the task {0}-{1} is in the wrong type'.format(task_type, task_url))
    task.delete()


def get_task_message():
    """
    get one task from the task sqs queue.
    and convert it from json to python structure
    :return: one sqs message
    """
    tasks = task_sqs.receive_messages(1)
    if len(tasks) > 0:
        task = tasks[0]
        return json.loads(task)
    else:
        return None


def run():
    """
    this is the worker main loop,
    will stop only when the worker is shutdown
    :return: None
    """
    while True:
        task = get_task_message()
        if task:
            implement_task()


def worker_main():
    """
    first the main deploy in EC2 (install all the dependency
    then import all the packages
    the call the main loop aka run
    :return: None
    """
    log.info('worker start is life cycle')
    run()


if __name__ == "__main__":
    worker_main()



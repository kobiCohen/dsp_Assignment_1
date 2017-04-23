import boto3
from logger.logger import Logger
from pdf_to_htm import ConvetToHtml
from pdf_to_img import ConvetToImg
from pdf_to_txt import ConvetToTxt

sqs = boto3.resource('sqs')
task_sqs = sqs.get_queue_by_name('task')
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
    the queue
    :return: one sqs message
    """
    tasks = task_sqs.receive_messages(1)
    if len(tasks) > 0:
        task = tasks[0]
        return task
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
    run()


if __name__ == "__main__":
    worker_main()


    # In [3]: sqs = boto3.resource('sqs', region_name='eu-central-1')
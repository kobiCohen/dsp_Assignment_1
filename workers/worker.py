import boto3
import json
import urllib2
from logger.logger import Logger
from setting import download_pdf_dic, convert_pdf_dic
from pdf_to_htm import pdf_to_html
from pdf_to_img import pdf_to_png
from pdf_to_txt import pdf_to_txt
from subprocess import check_call


sqs = boto3.resource('sqs')
task_sqs = sqs.create_queue(QueueName='task')
log = Logger()


def upload_file_to_s3():
    pass


def clean_pdf_folder():
    """
    clean the pdf download folder and result folder
    :return: None
    """
    check_call(['sudo', 'rm', '-r', '{0}/'.format(download_pdf_dic)])
    check_call(['sudo', 'rm', '-r', '{0}/'.format(convert_pdf_dic)])


def download_pdf(task_pdf, pdf_name):
    """
    download the file from the web
    :param task_pdf: list of [task_type, pdf_url]
    :return: None
    """
    response = urllib2.urlopen(task_pdf)
    with open('{0}/{1}.pdf'.format(download_pdf_dic, pdf_name), 'w') as pdf_file:
        pdf_file.write(response.read())


def implement_task(task):
    """
    implement task the pdf task
    :param task: json string [task_type, pdf_url]
    :return: None
    """
    clean_pdf_folder()
    # convert json string to python object
    task_type, task_url = json.loads(task.body)
    # parser the pdf name from pdf_url
    pdf_name = task_url.split('/')[-1][:-4]
    download_pdf(task_url, pdf_name)
    if task_type == 'ToImage':
        pdf_to_html(pdf_name)
    elif task_type == 'ToHTML':
        pdf_to_png(pdf_name)
    elif task_type == 'ToText':
        pdf_to_txt(pdf_name)
    else:
        log.warning('the task {0}-{1} is known type'.format(task_type, task_url))
    upload_file_to_s3()
    task.delete()


def get_task_message():
    """
    get one task from the task sqs queue.
    and convert it from json to python structure
    :return: one sqs message
    """
    task = task_sqs.receive_messages(1)
    if len(task) > 0:
        return task[0]
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
            implement_task(task)


def worker_main():
    """
    first the main deploy in EC2 (install all the dependency
    then import all the packages
    the call the main loop aka run
    :return: None
    """
    log.info('worker start is life cycle')
    run()

# you will enter the if statement only when the module is main
if __name__ == "__main__":
    worker_main()



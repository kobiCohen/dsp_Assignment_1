
import json
import urllib2
from subprocess import check_call
# this is a small hack so the worker will add the working dic to the sys file path
import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from logger.logger import Logger
from pdf_to_htm import pdf_to_html
from pdf_to_img import pdf_to_png
from pdf_to_txt import pdf_to_txt
from global_setting.setting import download_pdf_dic, convert_pdf_dic
from global_setting.sqs import done_pdf_tasks, new_pdf_tasks
from global_setting.s3 import upload_file

log = Logger('worker')


def send_done_message(pdf_loc_in_s3, task_type, task_url, task_group_id):
    """
    send to the done pdf task a done messge int the format 
    [pdf_loc_in_s3, task_type, task_url]
    :param pdf_loc_in_s3:  the loc in s3
    :param task_type:  the type to html and etc
    :param task_url:  the url of the pdf
    :param task_group_id: the id for the return
    :return: None
    """
    message = '[{0}, {1}, {2}, {3}]'.format(task_type, pdf_loc_in_s3, task_url, task_group_id)
    done_pdf_tasks.send_message(MessageBody=message)


def upload_file_to_s3(pdf_name, operation_type):
    """
    tar new object and upload it to s3
    :param pdf_name: the pdf name
    :param operation_type: 
    :return: return a string, where the file is in s3 
    """
    tar_name = '{0}.tar.gz'.format(pdf_name)
    tar_full_path = '{0}/{1}'.format(convert_pdf_dic, tar_name)
    check_call('tar -cvzf {0} {1}/* --remove-files'.format(tar_full_path, convert_pdf_dic), shell=True)
    s3_file_loc = '{0}/{1}'.format(operation_type, tar_name)
    upload_file(tar_full_path, s3_file_loc)
    return s3_file_loc


def clean_pdf_folder():
    """
    clean the pdf download folder and result folder
    then recreate them
    :return: None
    """
    check_call('sudo rm -fr {0}'.format(download_pdf_dic), shell=True)
    check_call('sudo rm -fr {0}'.format(convert_pdf_dic), shell=True)
    check_call('mkdir -p {0}'.format(download_pdf_dic), shell=True)
    check_call('mkdir -p {0}'.format(convert_pdf_dic), shell=True)


def download_pdf(task_pdf, pdf_name):
    """
    download the file from the web
    :param task_pdf: list of [task_type, pdf_url]
    :return: if download successfully return True otherwise false
    """
    try:
        response = urllib2.urlopen(task_pdf)
    except Exception as ex:
        log.exception(ex)
        return False
    log.info('download {} successfully'.format(pdf_name))
    with open('{0}/{1}.pdf'.format(download_pdf_dic, pdf_name), 'w+') as pdf_file:
        pdf_file.write(response.read())
    return True


def implement_task(task):
    """
    implement task the pdf task
    :param task: json string [task_type, pdf_url, task_group_id]
    :return: None
    """
    clean_pdf_folder()
    # convert json string to python object
    task_type, task_url, task_group_id = json.loads(task.body)
    log.info('received new task {0} {1} {2}'.format(task_type, task_url, task_group_id))
    # parser the pdf name from pdf_url
    pdf_name = task_url.split('/')[-1][:-4]
    if download_pdf(task_url, pdf_name) is True:
        try:
            if task_type == 'ToImage':
                pdf_to_png(pdf_name)
            elif task_type == 'ToHTML':
                pdf_to_html(pdf_name)
            elif task_type == 'ToText':
                pdf_to_txt(pdf_name)
            else:
                log.warning('the task {0}-{1} is of unknown type'.format(task_type, task_url))
                task.delete()

            pdf_loc_in_s3 = upload_file_to_s3(pdf_name, task_type)
            log.info('done with pdf {0}-{1} sending message'.format(task_type, task_url))
            send_done_message(pdf_loc_in_s3, task_type, task_url, task_group_id)
        except Exception as ex:
            # if the operation failed exit and don't delete the message
            log.exception(ex)
            return False
        task.delete()
    else:
        # if you cant download the pdf from the web delete the sqs message
        task.delete()


def get_task_message():
    """
    get one task from the task sqs queue.
    :return: one sqs message and if the queue os empty return None
    """
    task = new_pdf_tasks.receive_messages(1)
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
    first the main deploy_worker.txt in EC2 (install all the dependency
    then import all the packages
    the call the main loop aka run
    :return: None
    """
    log.info('worker start is life cycle')
    run()

# you will enter the if statement only when the module is main
if __name__ == "__main__":
    try:
        worker_main()
    except Exception as ex:
        log.exception(ex, info='this Exception is main, the worker cant recover \n good but cruel world')



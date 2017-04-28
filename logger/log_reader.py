import boto3
import botocore
import logging
import sys
import os


# this is a small hack so the worker will add the working dic to the sys file path
cwd = os.getcwd()
sys.path.append(cwd)

from global_setting.sqs import info_sqs, warning_sqs, critical_sqs

log = logging.getLogger('dsp')


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


def clean_old_logs():
    for qeue in [info_sqs, warning_sqs, critical_sqs]:
        try:
            qeue.purge()
        except Exception as ex:
            print ex


def build_logger():
    clean_old_logs()
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)


def read_info():
    message = get_new_message(info_sqs)
    if message:
        log.info(message.body)
        message.delete()


def read_warning():
    message = get_new_message(warning_sqs)
    if message:
        log.warning(message.body)
        message.delete()


def read_critical():
    message = get_new_message(critical_sqs)
    if message:
        log.critical(message.body)
        message.delete()


def main_loop():
    while True:
        read_info()
        read_warning()
        read_critical()


def main():
    build_logger()
    main_loop()


if __name__ == '__main__':
    main()

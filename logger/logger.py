import boto3
import socket
import traceback
from global_setting.sqs import info_sqs, warning_sqs, critical_sqs
import time


class Logger(object):

    def __init__(self, machine_job):
        # get the machine ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.machine_job = machine_job

    def info(self, message):
        message = self._create_message(message)
        info_sqs.send_message(MessageBody=message)

    def warning(self, message):
        message = self._create_message(message)
        warning_sqs.send_message(MessageBody=message)

    def critical(self, message):
        message = self._create_message(message)
        critical_sqs.send_message(MessageBody=message)

    def exception(self, ex, info=''):
        message = 'exception type: {type}\n ' \
                  'exception arguments: {arg}\n ' \
                  'message{str} \n\n\n ' \
                  '\t bt: \n {bt}'\
            .format(type=type(ex),
                    arg=ex.args,
                    str=ex,
                    bt=traceback.extract_stack())
        # append the two strings
        new_message = self._create_message(info + '\n' + message)
        critical_sqs.send_message(MessageBody=new_message)

    def _create_message(self, message):
        new_message = '{job}-{ip}:{message}'\
            .format(job=self.machine_job, ip=self.ip, message=message)
        return new_message

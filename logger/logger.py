import boto3
import socket
from global_setting.sqs import info_sqs, warning_sqs, critical_sqs

class Logger(object):

    def __init__(self, machine_job):
        # get the machine ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.machine_job = machine_job

    def info(self, message):
        message = self.create_message(message)
        info_sqs.send_message(MessageBody=message)

    def warning(self, message):
        message = self.create_message(message)
        warning_sqs.send_message(MessageBody=message)

    def critical(self, message):
        message = self.create_message(message)
        critical_sqs.send_message(MessageBody=message)

    def create_message(self, message):
        new_message = '{job}-{ip}:{message}'\
            .format(job=self.machine_job, ip=self.ip, message=message)
        return new_message

import boto3
import socket


class Logger(object):

    def __init__(self, machine_job):
        # get the machine ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.machine_job = machine_job
        sqs = boto3.resource('sqs')
        self.info_sqs = sqs.create_queue(QueueName='info_sqs')
        self.warning_sqs = sqs.create_queue(QueueName='warning_sqs')
        self.critical_sqs = sqs.create_queue(QueueName='critical_sqs')

    def info(self, message):
        message = self.create_message(message)
        self.info_sqs.send_message(MessageBody=message)

    def warning(self, message):
        message = self.create_message(message)
        self.warning_sqs.send_message(MessageBody=message)

    def critical(self, message):
        message = self.create_message(message)
        self.critical_sqs.send_message(MessageBody=message)

    def create_message(self, message):
        new_message = '{job}-{ip}:{message}'\
            .format(job=self.machine_job, ip=self.ip, message=message)
        return new_message

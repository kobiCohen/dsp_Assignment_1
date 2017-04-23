import boto3
import socket


class Logger(object):

    def __init__(self):
        # get the machine ip
        self.ip = socket.gethostbyname(socket.gethostname())
        sqs = boto3.resource('sqs')
        self.info_sqs = sqs.create_queue(QueueName='info')
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
        new_message = '{ip}:{message}'.format(ip=self.ip, message=message)
        return new_message

import boto3


class Logger(object):

    def __init__(self):
        sqs = boto3.resource('sqs')
        self.info_sqs = sqs.create_queue('info')
        self.warning_sqs = sqs.create_queue('warning_sqs')
        self.critical_sqs = sqs.create_queue('critical_sqs')

    def info(self, message):
        self.info_sqs.send_message(MessageBody=message)

    def warning(self, message):
        self.warning_sqs.send_message(MessageBody=message)

    def critical(self, message):
        self.critical_sqs.send_message(MessageBody=message)

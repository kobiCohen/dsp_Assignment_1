import boto3

sqs = boto3.resource('sqs')

new_task = sqs.create_queue(QueueName='new_task', Attributes={'VisibilityTimeout': '30'})
done_task = sqs.create_queue(QueueName='done_task', Attributes={'VisibilityTimeout': '30'})
new_pdf_tasks = sqs.create_queue(QueueName='new_pdf_task', Attributes={'VisibilityTimeout': '30'})
done_pdf_tasks = sqs.create_queue(QueueName='done_pdf_task', Attributes={'VisibilityTimeout': '30'})
info_sqs = sqs.create_queue(QueueName='info_sqs')
warning_sqs = sqs.create_queue(QueueName='warning_sqs')
critical_sqs = sqs.create_queue(QueueName='critical_sqs')


def purge_all_queue():
    for queue in [new_task, done_task, new_pdf_tasks, done_pdf_tasks, info_sqs, warning_sqs, scritical_sqs]:
        try:
            queue.purge()
        except boto3.ClientError as ex:
            #TODO: add print to logger
            pass

import boto3

sqs = boto3.resource('sqs')


new_task = sqs.create_queue(QueueName='new_task', Attributes={'VisibilityTimeout': '60'})
done_task = sqs.create_queue(QueueName='done_task', Attributes={'VisibilityTimeout': '60'})
new_pdf_tasks = sqs.create_queue(QueueName='new_pdf_task', Attributes={'VisibilityTimeout': '60'})
done_pdf_tasks = sqs.create_queue(QueueName='done_pdf_task', Attributes={'VisibilityTimeout': '60'})
info_sqs = sqs.create_queue(QueueName='info_sqs')
warning_sqs = sqs.create_queue(QueueName='warning_sqs')
critical_sqs = sqs.create_queue(QueueName='critical_sqs')


def purge_all_queue():
    """
    clean all the sqs queue
    :return: None
    """
    for queue in [new_task, done_task, new_pdf_tasks, done_pdf_tasks, info_sqs, warning_sqs, critical_sqs]:
        try:
            queue.purge()
        except boto3.ClientError:
            pass


def get_sqs_queue(queue_name):
    """
    get or create a new sqs
    :param queue_name: string -> the wanted name of the queue
    :return: new aws sqs object 
    """
    return sqs.create_queue(QueueName=queue_name)

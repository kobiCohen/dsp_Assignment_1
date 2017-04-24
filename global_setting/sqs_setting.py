import boto3

sqs = boto3.resource('sqs')

new_task = sqs.create_queue(QueueName='new_task', Attributes={'VisibilityTimeout': '30'})
done_task = sqs.create_queue(QueueName='done_task', Attributes={'VisibilityTimeout': '30'})
new_pdf_tasks = sqs.create_queue(QueueName='new_pdf_task', Attributes={'VisibilityTimeout': '30'})
done_pdf_tasks = sqs.create_queue(QueueName='done_pdf_task', Attributes={'VisibilityTimeout': '30'})



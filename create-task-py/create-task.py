import boto3
import random

def handler(event, context):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id='nKRSTJ2RtVi5adaSim-_',
        aws_secret_access_key='gpzr1qkECWFfdNV798emZZBIsbNXdP3DLi-ehTJm'
    )

    name = str(random.randint(1000, 9999)) + '.jpg'
    url = s3.generate_presigned_post('upload-bucket-hw7', name, ExpiresIn=3600)

    queue = session.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id='nKRSTJ2RtVi5adaSim-_',
        aws_secret_access_key='gpzr1qkECWFfdNV798emZZBIsbNXdP3DLi-ehTJm'
    )

    queue_url = 'https://message-queue.api.cloud.yandex.net/b1gsqouokhlqp1j2bo7r/dj6000000001o02q007d/file-name-queue'
    queue.send_message(
        QueueUrl=queue_url,
        MessageBody=name
    )

    return {
        'statusCode': 200,
        'body': url,
    }
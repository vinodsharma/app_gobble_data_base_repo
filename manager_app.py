import pika
import src.app_utils.settings as settings
import os
import boto3
import logging
import sys

url = "amqp://ulclrorr:a-HMtnXgFep9mK-x03rr-982kPRuqKCz@hornet.rmq.cloudamqp.com/ulclrorr"
url_with_timeout = url + "?socket_timeout=10"
connection = pika.BlockingConnection(pika.URLParameters(url_with_timeout))
channel = connection.channel()

exchange = 'gobble-development'
queue = 'sorting-hat-queue'

channel.exchange_declare(exchange=exchange, exchange_type='topic')
channel.queue_declare(queue=queue, durable=True)

binding_keys = ["gobble.regionalmenu.approved"]
for binding_key in binding_keys:
    channel.queue_bind(exchange=exchange,
                       queue=queue,
                       routing_key=binding_key)

def get_deploy_settings():
    deploy_settings = {
            'DOCKER_IMAGE': os.getenv('DOCKER_IMAGE'),
    }
    deploy_settings.update(settings.get_settings_dict())
    return deploy_settings


def submit_job(batch_client, job_definition_name, job_name,
                job_queue_name, env_variables):
    response = batch_client.submit_job(
        jobDefinition=job_definition_name,
        jobName=job_name,
        jobQueue=job_queue_name,
        containerOverrides={
            'environment': env_variables,
        },
    )
    print('Submit job response %s', response)


def create_batch_job_env_variables(event):
    env_variables = []
    for key, value in event.items():
        env_variables.append({'name': key, 'value': str(value)})
    return env_variables


def start_aws_batch_job():
    print("Job Submit Started")
    job_queue_name = 'app_gobble_data_base_repo_job_queue'
    job_definition_name = 'app_gobble_data_base_repo_job_definition'
    job_name = 'app_gobble_data_base_repo_job'
    event = get_deploy_settings()
    env_variables = create_batch_job_env_variables(event)
    batch_client = boto3.client('batch')
    submit_job(batch_client, job_definition_name, job_name,
                job_queue_name, env_variables)
    print("Job Submit Ended")

start_aws_batch_job()

def callback(ch, method, properties, body):
    print("Received %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)


print('Waiting for Messages. To exit press CTRL+C')
channel.start_consuming()

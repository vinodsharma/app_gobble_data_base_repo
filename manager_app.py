import pika
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

print('Waiting for Messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("Received %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue,
                      no_ack=True)

channel.start_consuming()

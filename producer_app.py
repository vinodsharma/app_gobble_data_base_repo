import pika
import sys

url = "amqp://127.0.0.1"
url_with_timeout = url + "?socket_timeout=10"
connection = pika.BlockingConnection(pika.URLParameters(url_with_timeout))
channel = connection.channel()

exchange = 'gobble-development'
channel.exchange_declare(exchange=exchange, exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'unknown.unknown.uknown'
message = ' '.join(sys.argv[2:]) or 'Unknown!'
channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2,
                      ))
print("Sent %r:%r" % (routing_key, message))
connection.close()


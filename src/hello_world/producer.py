from pika import channel
import os

import pika
from dotenv import load_dotenv

load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))

channel = connection.channel()

channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close()
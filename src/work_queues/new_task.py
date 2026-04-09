import os
import random

import pika
from dotenv import load_dotenv

load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

random_words = ["Discombobulating", "Concocting","Pontificating", "Tomfoolering", "Waddling", "Reticulating","Bloviating", "Whatchamacalliting"]

# write a code to generate a random message with random words with dots appended
message = ''.join(random.choice(random_words)) + "." * random.randint(1, 10)

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))

channel = connection.channel()

channel.queue_declare(queue='hello', durable=True,
                      arguments={'x-queue-type': 'quorum'})

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=pika.DeliveryMode.Persistent,
                      )
                    )

print(f" [x] Sent '{message}'")

connection.close()

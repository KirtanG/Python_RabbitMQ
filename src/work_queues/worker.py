import os
import sys
import time

import pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")

def main():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))

    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

    channel.basic_consume(
        queue='hello',
        auto_ack=True,
        on_message_callback=callback,
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("[*] Exiting...")
        sys.exit(0)


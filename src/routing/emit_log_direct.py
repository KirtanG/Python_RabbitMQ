import os
import sys
import random
import asyncio

import aio_pika
from dotenv import load_dotenv


load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")


async def main():

    connection = await aio_pika.connect_robust(RABBITMQ_URI)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(name="direct_exchange",type=aio_pika.ExchangeType.DIRECT,durable=False)

    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'

    await exchange.publish(message=aio_pika.Message(
        body=message.encode(),
        delivery_mode=aio_pika.DeliveryMode.NOT_PERSISTENT
    ),routing_key=severity)

    print(f" [x] Sent {severity}:{message}")

    await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
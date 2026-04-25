import os
import asyncio

import aio_pika
from dotenv import load_dotenv

load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URI)

    async with connection.channel() as channel:
        await channel.declare_queue(
            name='hello',
            durable=True,
            arguments={
                'x-queue-type':'quorum'
            }
        )

        await channel.default_exchange.publish(
            routing_key = 'hello',
            message = aio_pika.Message(
                body = "yooo!".encode(),
                delivery_mode = aio_pika.DeliveryMode.PERSISTENT # same as in tutorial for durable = True
            ),

        )

        await connection.close()
    print(" [x] Sent 'Hello World!'")

if __name__ == "__main__":
    asyncio.run(main())
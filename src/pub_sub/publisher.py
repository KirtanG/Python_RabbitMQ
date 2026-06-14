import os
import random
import asyncio

import aio_pika
from dotenv import load_dotenv

load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("""RABBITMQ_URI is not set""")

random_words = [
    "Discombobulating", "Concocting", "Pontificating", "Tomfoolering",
    "Waddling", "Reticulating", "Bloviating", "Whatchamacalliting"
]

async def main():
    # Generate a random message: word + random number of dots (1-10)
    word = random.choice(random_words)
    dots = "." * random.randint(1, 10)
    message = word + dots

    connection = await aio_pika.connect_robust(RABBITMQ_URI)

    async with connection.channel() as channel:
        exchange = await channel.declare_exchange(
            name="logs",
            type=aio_pika.ExchangeType.FANOUT,
            durable=False
        )

        message = aio_pika.Message(
            body=message.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )  

        await exchange.publish(message=message,routing_key='')

        print(f" [x] Sent {message.body}")  

    await connection.close()

if __name__ == "__main__":
    asyncio.run(main())
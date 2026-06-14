import os
import sys
import asyncio

import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

async def callback(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process(ignore_processed=True):
        body = message.body
        print(f" [x] Received {body}")

async def main():
    print("Starting...")
    async with await aio_pika.connect_robust(RABBITMQ_URI) as connection:

        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            name="logs",
            type=aio_pika.ExchangeType.FANOUT
        )

        queue = await channel.declare_queue(
            name='',
            exclusive=True
        )

        await queue.bind(
            exchange=exchange
        )

        await queue.consume(
            callback=callback,
            no_ack=True
        )


        print(' [*] Waiting for logs. To exit press CTRL+C')
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print("Terminating consumer....")
            await connection.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n")
        print("[*] Exiting...")
        sys.exit(0)
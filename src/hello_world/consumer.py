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
    async with message.process():
        body = message.body
        print(f" [x] Received {body}")

async def main():
    print("Starting....")
    connection = await aio_pika.connect_robust(RABBITMQ_URI)
    print("Connection done!")
    async with connection.channel() as channel:
        await channel.declare_queue(
            name='hello', 
            durable=True, 
            arguments={'x-queue-type': 'quorum'}
        )

        # start consuming the event
        queue = await channel.get_queue(name="hello")
        await queue.consume(
            callback=callback,
            no_ack=False
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
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


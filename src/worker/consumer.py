import os
import sys
import asyncio

import aio_pika
from dotenv import load_dotenv


load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

async def on_message( message:aio_pika.IncomingMessage) -> None:

    async with message.process(ignore_processed=True):

        body_str = message.body.decode()

        print(f" [x] Recevied Message:{body_str}")

        dot_count = body_str.count('.')
        await asyncio.sleep(dot_count)

        print(" [X] Done")

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

        await channel.set_qos(prefetch_count=1)

        queue = await channel.get_queue(name='hello')

        await queue.consume(on_message,no_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        
        try:
            await asyncio.Future()  
        except asyncio.CancelledError:
            print("\n[*] Exiting...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
        sys.exit(0)



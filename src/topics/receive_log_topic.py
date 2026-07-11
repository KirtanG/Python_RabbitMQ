import os
import sys
import asyncio

import aio_pika
from dotenv import load_dotenv

load_dotenv(".env")

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set!")

async def receive_message(message:aio_pika.abc.AbstractIncomingMessage):
    
    async with message.process(ignore_processed=True):
        body_str = message.body.decode()
        routing_key = message.routing_key
        print(f" [x] {routing_key}:{body_str}")
    

async def main():
    
    # Check command‑line arguments (at least one severity)
    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)
    
    async with await aio_pika.connect_robust(url=RABBITMQ_URI) as connection:

        async with connection.channel() as channel:
            exchange = await channel.declare_exchange(
            name="topic_logs",
            type=aio_pika.ExchangeType.TOPIC,
            durable=False
        )

            queue = await channel.declare_queue(
            name='',
            exclusive=True
        )
         # Bind the queue to each severity (routing key)
            for binding_key in binding_keys:
                await queue.bind(exchange, routing_key=binding_key)

            print(' [*] Waiting for logs. To exit press CTRL+C')

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await receive_message(message)

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
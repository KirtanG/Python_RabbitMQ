import os
import sys
import asyncio
from functools import partial


import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")

def remote_fibonnaci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return remote_fibonnaci(n-1) + remote_fibonnaci(n - 2)

async def on_request(message: aio_pika.abc.AbstractIncomingMessage, channel: aio_pika.Channel) -> None:

    async with message.process(ignore_processed=True):
        try:
            n = int(message.body)
            print(f" [.] Recevied :{n}")
        except ValueError:
            print(f"Recevied Invalid Value {message.body}")
            return
    
        result = remote_fibonnaci(n)
        # Publish the response to the reply_to queue
        # Use the correlation_id from the request
        await channel.default_exchange.publish(
            message=aio_pika.Message(
                body=str(result).encode(),
                correlation_id=message.correlation_id
            ),
            routing_key = message.reply_to or ""
        )


    

async def main() -> None:
    
    connection = await aio_pika.connect_robust(url = RABBITMQ_URI)
    async with await connection.channel()  as channel:
        await channel.declare_queue(
            name="rpc_queue",
            durable=True,
            arguments={
                'x-queue-type':'quorum'
            }
        )

        # Prefetch 1 – fair dispatch
        await channel.set_qos(prefetch_count=1)

        # Get the queue and start consuming
        queue = await channel.get_queue(name='rpc_queue')

        # Use partial to inject the channel argument into the callback
        bound_callback = partial(on_request,channel=channel)

        await queue.consume(bound_callback, no_ack=False) # manual ack via context

        print(" [x] Awaiting RPC requests")
        # Keep the server running
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            print(" [x] Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n [x] Exiting...")
        sys.exit(0)
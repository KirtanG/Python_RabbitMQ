import os
import queue
from re import L
import sys
from tkinter import N
from unittest import result
import uuid
import asyncio

import aio_pika
from aiormq import connect
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URI = os.getenv("RABBITMQ_URI")

if not RABBITMQ_URI:
    raise RuntimeError("RABBITMQ_URI is not set")



class FibonacciRpcClient(object):

    def __init__(self,loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}

    async def connect(self) -> None:
        """Establish connection, create channel, and declare callback queue."""
        self.connection = await aio_pika.connect_robust(RABBITMQ_URI)
        self.channel = await self.connection.channel()
        # Declare exclusive, server‑named queue
        self.callback_queue = await self.channel.declare_queue('',exclusive=True)
        # Start consuming from callback queue, with manual ack (we'll ack inside callback)
        await self.callback_queue.consume(self.on_response,False)

    async def on_response(self,message: aio_pika.IncomingMessage) -> None:
        """Callback when a response arrives on the callback queue."""
        future = self.futures.get(message.correlation_id)
        if future and not future.done():
            # Set the result (the message body) and ack the message
            future.set_result(message.body)
            await message.ack()
        else:
            # Unknown correlation id – just ack and discard
            await message.ack()
    
    async def call(self, n:int ) -> int:
        """Send an RPC request and wait for the response asynchronously."""
        # Generate a unique correlation_id
        corr_id = str(uuid.uuid4())
        # Create a Future that will be completed when the response arrives
        future = self.loop.create_future()
        self.futures[corr_id] = future 

        # Publish the request to the rpc_queue
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body= str(n).encode(),
                correlation_id= corr_id,
                reply_to=self.callback_queue.name
            ),
            routing_key='rpc_queue'
        )

        try:
            response_body = await asyncio.wait_for(future, timeout=30.0)
            return int(response_body.decode())
        except asyncio.TimeoutError:
            # Handle timeout: remove the future and raise an exception
            self.futures.pop(corr_id, None)
            raise TimeoutError("RPC call timed out")
        finally:
            # Clean up the future (if still there)
            self.futures.pop(corr_id, None)

async def main():
    loop = asyncio.get_running_loop()
    client = FibonacciRpcClient(loop)
    await client.connect()

    # Change the number
    n = 15

    print(f" [x] Requesting fib({n})")
    try:
        response = await client.call(n)
        print(f" [.] Got {response}")
    except TimeoutError as e:
        print(f" [x] RPC failed: {e}")

    # Close the connection gracefully
    await client.connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n [x] Exiting...")
        sys.exit(0)

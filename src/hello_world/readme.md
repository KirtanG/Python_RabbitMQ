## Hello World Example 

Link: https://www.rabbitmq.com/tutorials/tutorial-one-python

## Key Takeaways

1. Producing means nothing more than sending. A program that sends messages is a producer.

2. A queue is the name for the post box in RabbitMQ. Although messages flow through RabbitMQ and your applications, they can only be stored inside a queue. A queue is only bound by the host's memory & disk limits, it's essentially a large message buffer. Many producers can send messages that go to one queue, and many consumers can try to receive data from one queue.

3. Consuming has a similar meaning to receiving. A consumer is a program that mostly waits to receive messages.
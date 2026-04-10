# Python with RabbitMQ

This repo contains source code of exploration of Python with RabbitMQ.

## Exchanges 

The core idea in the messaging model in RabbitMQ is that the producer never sends any messages directly to a queue. Actually, quite often the producer doesn't even know if a message will be delivered to any queue at all.

Instead, the producer can only send messages to an exchange. An exchange is a very simple thing. On one side it receives messages from producers and on the other side it pushes them to queues. The exchange must know exactly what to do with a message it receives. Should it be appended to a particular queue? Should it be appended to many queues? Or should it get discarded. The rules for that are defined by the exchange type.

There are a few exchange types available: `direct`, `topic`, `headers` and `fanout`.

## Bindings

That relationship between exchange and a queue is called a binding.

## Direct exchange



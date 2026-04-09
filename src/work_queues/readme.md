## Work Queues Example

Link: https://www.rabbitmq.com/tutorials/tutorial-two-python

## Key Takeaways

The main idea behind Work Queues (aka: Task Queues) is to avoid doing a resource-intensive task immediately and having to wait for it to complete. Instead we schedule the task to be done later. We encapsulate a task as a message and send it to the queue. A worker process running in the background will pop the tasks and eventually execute the job. When you run many workers the tasks will be shared between them.

This concept is especially useful in web applications where it's impossible to handle a complex task during a short HTTP request window.

###  Round-robin dispatching
One of the advantages of using a Task Queue is the ability to easily parallelise work. If we are building up a backlog of work, we can just add more workers and that way, scale easily.

### Message acknowledgment
Without message acknowledgment, if a worker crashes, the message it was processing is lost. To prevent this, we can use message acknowledgment. When a worker receives a message, it acknowledges it to the broker. If the worker crashes, the message is not acknowledged and is redelivered to another worker.

### Message Durability
When RabbitMQ quits or crashes it will forget the queues and messages unless you tell it not to. Two things are required to make sure that messages aren't lost: we need to mark both the queue and messages as durable.

### Fair dispatch
when all odd messages are heavy and even messages are light, one worker will be constantly busy and the other one will do hardly any work. Well, RabbitMQ doesn't know anything about that and will still dispatch messages evenly.

This happens because RabbitMQ just dispatches a message when the message enters the queue. It doesn't look at the number of unacknowledged messages for a consumer. It just blindly dispatches every n-th message to the n-th consumer.
Instead, it will dispatch it to the next worker that is not still busy.
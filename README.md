# Python with RabbitMQ

This repository contains exploration code of Python with RabbitMQ utilizing `aio_pika`. The codebase is structured around the official RabbitMQ tutorials, transitioning from a basic "Hello World" example to a Remote Procedure Call (RPC) pattern.

## Prerequisites

- Python 3.11+
- A running RabbitMQ broker
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`

## Configuration

Create a `.env` file in the root directory (a sample is provided):

```env
RABBITMQ_URI=amqp://username:password@localhost:5672
```

## Setup

Using **uv**:
```bash
uv sync
```

Using standard **pip**:
```bash
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -e .
```

## Tutorials & Usage

Each tutorial includes a producer (publisher/client) and a consumer (subscriber/server). Run each component in separate terminal windows.

### 1. Hello World
A basic producer that sends a single message, and a consumer that receives it.
* **Consumer**:
  ```bash
  uv run python src/hello_world/consumer.py
  ```
* **Producer**:
  ```bash
  uv run python src/hello_world/producer.py
  ```

### 2. Work Queues (Task Queue)
Distributing time-consuming tasks among multiple workers.
* **Consumer (Worker)**:
  ```bash
  uv run python src/worker/consumer.py
  ```
* **Producer (New Task)**:
  ```bash
  uv run python src/worker/producer.py
  ```

### 3. Publish/Subscribe
Delivering a message to multiple consumers using a fanout exchange.
* **Subscriber**:
  ```bash
  uv run python src/pub_sub/subscriber.py
  ```
* **Publisher**:
  ```bash
  uv run python src/pub_sub/publisher.py
  ```

### 4. Routing
Receiving messages selectively using a direct exchange.
* **Consumer (Log Receiver)**:
  ```bash
  uv run python src/routing/receive_logs_direct.py [info] [warning] [error]
  ```
* **Producer (Log Emitter)**:
  ```bash
  uv run python src/routing/emit_log_direct.py [severity] [message]
  ```

### 5. Topics
Receiving messages selectively based on wildcard routing keys.
* **Consumer**:
  ```bash
  uv run python src/topics/receive_log_topic.py "*.critical" "kern.*"
  ```
* **Producer**:
  ```bash
  uv run python src/topics/emit_log_topic.py "kern.critical" "A critical kernel error occurred."
  ```

### 6. Remote Procedure Call (RPC)
A request-response pattern to run a function on a remote computer and wait for the result.
* **Server**:
  ```bash
  uv run python src/rpc/rpc_server.py
  ```
* **Client**:
  ```bash
  uv run python src/rpc/rpc_client.py
  ```

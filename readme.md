# RabbitMQ Order Processing System

This repository demonstrates a RabbitMQ-based system for order processing. The project is composed of three main components:

1. **`Consume_messages.py`**: A consumer that processes messages from a queue.
2. **`Send_messages.py`**: A producer that generates and sends order messages to the queue.
3. **`Test_producer.py`**: A pytest-based script to verify the producer's functionality.

## Prerequisites

Before running the code, ensure you have the following installed:

- Python 3.8 or later
- RabbitMQ Server
- Python packages listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Project Structure

```
.
├── Consume_messages.py  # Consumer script
├── Send_messages.py     # Producer script
├── Test_producer.py     # Test for producer
├── requirements.txt     # Python dependencies
```

## How to Use

### 1. Start RabbitMQ Server

Ensure RabbitMQ is running locally. For installation and setup, refer to the [official RabbitMQ documentation](https://www.rabbitmq.com/download.html).

### 2. Run the Producer

Generate and send an order message:

```bash
python Send_messages.py
```

### 3. Run the Consumer

Start the consumer to process messages from the queue:

```bash
python Consume_messages.py
```

### 4. Run Tests

Run the test suite to validate the producer functionality:

```bash
pytest Test_producer.py
```

## Features

- **Producer (`Send_messages.py`)**: Generates random order messages and sends them to the RabbitMQ queue.
- **Consumer (`Consume_messages.py`)**: Processes messages, simulates saving to a mock database, and acknowledges the messages.
- **Testing (`Test_producer.py`)**: Ensures messages are enqueued correctly and validates their content.

## Configuration

The queue name and connection parameters are hardcoded as `order_queue` and `localhost`, respectively. Update these values in the scripts if necessary.

## Example Output

### Producer Output

```bash
Order sent: {
    'order_id': 1234,
    'customer_id': 15,
    'order_date': '2024-12-07 10:30:00',
    'items': [...],
    'total_price': 3000.00,
    'status': 'created'
}
```

### Consumer Output

```bash
Waiting for messages...
Message received!
Processing order: {
    'order_id': 1234,
    'customer_id': 15,
    'order_date': '2024-12-07 10:30:00',
    'items': [...],
    'total_price': 3000.00,
    'status': 'created'
}
Order 1234 successfully processed!
```

## Troubleshooting

- **RabbitMQ not running**: Ensure the RabbitMQ server is started.
- **Queue not declared**: Verify that `order_queue` is declared in both producer and consumer scripts.
- **Message not processed**: Check for errors in the consumer script.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## requirements.txt

```text
pika
pytest
```

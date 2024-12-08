import pika
import time

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Verifica o número de mensagens na fila
queue_info = channel.queue_declare(queue='task_queue', passive=True)
messages_ready = queue_info.method.message_count  # Mensagens prontas para consumo
messages_unacknowledged = queue_info.method.consumer_count  # Mensagens não confirmadas

print(f"Mensagens prontas para consumo: {messages_ready}")
print(f"Mensagens não confirmadas: {messages_unacknowledged}")

# Fechar a conexão
connection.close()

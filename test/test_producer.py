import pika
import json
import pytest
from rabbitmq_files.send_messages_producer import send_messages  # Importa a função ou módulo do producer
import time  # Para adicionar delay se necessário

@pytest.fixture
def rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
    yield channel
    channel.queue_purge(queue='order_queue')  # Purga a fila após o teste
    connection.close()

def test_producer_functionality(rabbitmq_connection):
    # Dados do pedido para enviar, alinhados com a estrutura real gerada pela função generate_order_data()
    order_data = {
        "order_id": 3563,  # Um valor gerado aleatoriamente pelo produtor
        "customer_id": 15,
        "order_date": "2024-12-07 10:30:00",  # Data gerada pelo produtor
        "items": [
            {'product_id': 101, 'product_name': 'Laptop', 'quantity': 1, 'price': 1200},
            {'product_id': 102, 'product_name': 'Mouse', 'quantity': 2, 'price': 25},
            {'product_id': 103, 'product_name': 'Keyboard', 'quantity': 1, 'price': 80}
        ],
        "total_price": 3000.00,
        "status": "created"
    }

    # Verifique o número de mensagens antes de enviar a nova mensagem
    initial_queue_state = rabbitmq_connection.queue_declare(queue='order_queue', durable=True, passive=True)
    initial_message_count = initial_queue_state.method.message_count

    # Chama o produtor para enviar a mensagem
    send_messages(order_data)

    # Adiciona um pequeno delay para garantir que a mensagem tenha sido processada
    time.sleep(1)  # Ajuste conforme necessário

    # Verifica se a mensagem foi enviada (verificando a contagem da fila)
    queue_state = rabbitmq_connection.queue_declare(queue='order_queue', durable=True, passive=True)
    assert queue_state.method.message_count == initial_message_count + 1, "A mensagem não foi enviada para a fila!"

    # Consome a mensagem para validar o conteúdo
    method_frame, header_frame, body = rabbitmq_connection.basic_get(queue='order_queue', auto_ack=True)
    assert method_frame is not None, "Nenhuma mensagem foi encontrada na fila!"
    received_message = json.loads(body)
    print(received_message)
    print(order_data)


    # Valida se o conteúdo da mensagem é igual ao enviado
    assert received_message == order_data, "O conteúdo da mensagem enviada não corresponde ao esperado!"

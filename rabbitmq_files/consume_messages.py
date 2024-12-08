import pika
import json
import time

# Simulando um banco de dados
class MockDatabase:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_all_orders(self):
        return self.orders

# Função que simula o processamento do pedido
def process_order(ch, method, properties, body):
    print("Mensagem recebida!")
    try:
        # Converte os dados da mensagem (que estão no formato JSON) em um dicionário
        order_data = json.loads(body)
        print("Processando pedido:", order_data)

        # Simula o processamento, por exemplo, "salvando" o pedido em um banco de dados simulado
        mock_db = MockDatabase()
        mock_db.add_order(order_data)

        # Simula um tempo de processamento
        time.sleep(2)

        # Confirmando que a mensagem foi processada
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Pedido {order_data['order_id']} processado com sucesso!")
    except Exception as e:
        print("Erro no processamento:", str(e))
        # Não confirma a mensagem para que ela permaneça na fila
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consuming():
    try:
        # Estabelece a conexão com o RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declara a fila de pedidos
        channel.queue_declare(queue='order_queue', durable=True)

        # Define o pré-processamento de uma mensagem por vez
        channel.basic_qos(prefetch_count=1)

        # Define o que fazer quando uma mensagem for recebida
        channel.basic_consume(queue='order_queue', on_message_callback=process_order)

        print("Aguardando mensagens...")
        channel.start_consuming()
    except Exception as e:
        print("Erro ao iniciar o consumidor:", str(e))

if __name__ == "__main__":
    start_consuming()

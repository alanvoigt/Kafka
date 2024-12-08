import pika
import json
import random
import datetime

def generate_order_data():
    # Gera um ID de pedido único
    order_id = random.randint(1000, 9999)
    
    # Gera um cliente aleatório
    customer_id = random.randint(1, 100)
    
    # Itens do pedido
    items = [
        {'product_id': 101, 'product_name': 'Laptop', 'quantity': 1, 'price': 1200},
        {'product_id': 102, 'product_name': 'Mouse', 'quantity': 2, 'price': 25},
        {'product_id': 103, 'product_name': 'Keyboard', 'quantity': 1, 'price': 80}
    ]
    
    # Calcula o total do pedido
    total_price = sum(item['price'] * item['quantity'] for item in items)
    
    # Gera a data do pedido
    order_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Retorna os dados do pedido
    return {
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date,
        'items': items,
        'total_price': total_price,
        'status': 'created'
    }

def send_messages(order_data):
    # Estabelece conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara a fila de pedidos
    channel.queue_declare(queue='order_queue', durable=True)

    # Envia a mensagem com dados do pedido (convertido em JSON)
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Torna a mensagem persistente
        )
    )
    print("Pedido enviado:", order_data)
    connection.close()

if __name__ == "__main__":
    # Envia um pedido com dados gerados
    order_data = generate_order_data()
    send_messages(order_data)
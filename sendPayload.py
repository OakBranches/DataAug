import pika
import json

# Setup inicial do RabbitMQ
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port="5672",
        credentials=credentials
    )
)
channel = connection.channel()

channel.queue_declare(queue='payload')

# Abrindo o arquivo JSON
f = open('payload.json')

# Lendo o arquivo JSON
payload = json.load(f)

# Enviando as mensagens para a fila
for data in payload:
    channel.basic_publish(exchange='',
                      routing_key='payload',
                      body=json.dumps(data))
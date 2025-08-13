import json
import uuid

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import pika
import os
import time

app = Flask(__name__)
CORS(app, origins=["*"])

# Configuração do RabbitMQ (substitua pela sua URL do CloudAMQP ou local)
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqps://smzjygvv:ZZnn9lC-qQHQlOy3jR1JQ1_prAOyebu4@horse.lmq.cloudamqp.com/smzjygvv')
QUEUE_NAME = 'fila_exemplo'

# Conecta ao RabbitMQ uma vez no início
#params = pika.URLParameters(RABBITMQ_URL)
#connection = pika.BlockingConnection(params)
#channel = connection.channel()
#channel.queue_declare(queue=QUEUE_NAME, durable=True)

@app.route('/sse')
def sse():
    def event_stream():
        while True:
            data = {"time": time.strftime("%H:%M:%S")}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(20)
            break

    return Response(
        stream_with_context(event_stream()),
        content_type='text/event-stream'
    )

@app.route('/publicar', methods=['POST'])
def publicar():
    data = request.get_json()
    print(data)

    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    #if not data or 'mensagem' not in data:
    #    return jsonify({'erro': 'Campo "mensagem" é obrigatório'}), 400

    data['ip'] = ip
    data['uuid'] = str(uuid.uuid4())
    #mensagem = data['mensagem']
    mensagem = json.dumps(data)
    try:
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=mensagem.encode(),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        return jsonify({'status': 'Mensagem enviada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)

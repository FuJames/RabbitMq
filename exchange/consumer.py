import pika
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.21.236.94',port=5672, credentials=credentials))
channel = connection.channel()

result = channel.queue_declare(queue='report_impt_queue')
queue_name = result.method.queue

channel.queue_bind(exchange='report_impt_exchange',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
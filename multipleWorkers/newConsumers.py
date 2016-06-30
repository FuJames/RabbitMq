#coding:utf8
import pika
import time
# 运行多次newConsumers.py，就会产生多个consumer，取得的资源是互补且互斥的
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # RabbitMQ只有在收到consumer的确认消息后才会删除此消息
    ch.basic_ack(delivery_tag = method.delivery_tag)
# 优化多consumers时的任务分配，RabbitMQ如果发现当前consumer还有prefetch_count条message未确认时，就不会再给它塞消息；
# 默认情况下，RabbitMQ是轮询的给每个consumer发送消息
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
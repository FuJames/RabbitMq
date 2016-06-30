#coding:utf8
import pika
#connect to Rabbit MQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
# queue_declare 可以在consumer端做，也可以在producer端做，但Rabbit MQ针对一个queue名称只会维护一个queue
channel.queue_declare(queue='hello')
# routing_key与queue名称对应
channel.basic_publish(exchange='',routing_key='hello',body='hello world 6')

print '[x] sent "hello world" '

connection.close()
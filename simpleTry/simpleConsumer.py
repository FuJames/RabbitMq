#coding:utf8
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='hello')

def callBack(ch, method, properties, body):
    print ('[x] reveicve %r '%body)

channel.basic_consume(callBack,queue='hello',no_ack=True)
#consumer会一直监听queue，一旦有新的message则会进入callBack中执行；底层就是个Socket Server
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

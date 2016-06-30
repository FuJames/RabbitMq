# coding:utf8
import pika
import sys

# producer不能直接向queue发送消息，只能先向exchange发送消息，再由cousumer定义queue，并绑定某个exchange后，从queue取消息

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
# 定义一个名为logs的exchange，如果类型为fanout，exchange会把消息广播到所有的queue中；如果exchange类型为direct，那么exchange只会把消息发送
# 给与消息routing_key绑定的consumer
channel.exchange_declare(exchange='logs2',
                         type='direct')
# queue_declare可以在consumer端做，也可以在producer端做，但Rabbit MQ针对一个queue名称只会维护一个queue
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='black',  # message只会发送到与black绑定的queue
                      body=message)
print(" [x] Sent %r" % message)
connection.close()

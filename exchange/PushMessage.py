# coding:utf8
import pika
import json

# producer不能直接向queue发送消息，只能先向exchange发送消息，再由cousumer定义queue，并绑定某个exchange后，从queue取消息

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.21.236.94',port=5672, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='report_impt_exchange',
                         type='direct')

result = channel.queue_declare(queue='report_impt_queue')
queue_name = result.method.queue

channel.queue_bind(exchange='report_impt_exchange',
                   queue=queue_name)
# 定义一个名为logs的exchange，如果类型为fanout，exchange会把消息广播到所有的queue中；如果exchange类型为direct，那么exchange只会把消息发送
# 给与消息routing_key绑定的consumer

# queue_declare可以在consumer端做，也可以在producer端做，但Rabbit MQ针对一个queue名称只会维护一个queue
message = {"id":707155909835894,"announcement_id":2491535,"report_content_id":3099760,"report_class":"年度报告-财务披露","send_time":"2016-07-07 15:59:09"}
channel.basic_publish(exchange='report_impt_exchange',
                      routing_key='',  # message只会发送到与black绑定的queue
                      body=json.dumps(message))
print(" [x] Sent %r" % message)
connection.close()

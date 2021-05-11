import pika
import sys


class MetricsAPI(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)

    def push_metrics(self, ctxt, msg):
        time.sleep(0.001)
        call_context = self.client.prepare(version='1.0', fanout=True)

        return call_context.cast(ctxt,
                                 'push_metrics',
                                 msg=msg,
                                 )

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print(" [x] Sent %r" % message)
connection.close()

import time

import pika



class MetricsAPI(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='metrics_queue', durable=True)

    def push_metrics(self, ctxt, msg):
        time.sleep(0.001)
        self.channel.basic_publish(
            exchange='',
            routing_key='metrics_queue',
            body=str(msg),
            properties=pika.BasicProperties(delivery_mode=2)
        )





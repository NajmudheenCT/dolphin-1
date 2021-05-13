import pika
import time
import threading

from delfin import context

from delfin.exporter import base_exporter


class Consumer(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='metrics_queue', durable=True)
        self.perf_exporter = base_exporter.PerformanceExporterManager()
        self.total = 0

    def callback(self, ch, method, properties, body):
        # print(" [x] Received %r " % body)
        time.sleep(0.001)
        self.perf_exporter.dispatch(context, body)
        self.total += 1
        print("total metrics now:", self.total)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print(str(self.thread_name) + " " + str(self.thread_ID));

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='metrics_queue', on_message_callback=self.callback)

        self.channel.start_consuming()


thread1 = Consumer("metrics", 1000)
thread1.start()

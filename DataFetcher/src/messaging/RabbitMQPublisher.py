
import pika
from services.ConfigDistributer import ConfigDistributerService


class MQPublisher:



    def __init__(self):
        self.host = ConfigDistributerService.get_rabbitmq_config_data("RabbitMQ","host")
        self.port = ConfigDistributerService.get_rabbitmq_config_data("RabbitMQ","port")
        self.topic = ConfigDistributerService.get_rabbitmq_config_data("RabbitMQ","topic")



    @staticmethod
    def publish_all_list_in_single_connection(person_list):

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQPublisher().host, port=MQPublisher().port))
        channel =connection.channel()
        channel.queue_declare(queue=MQPublisher().topic, durable=True, arguments={'x-queue-type': 'quorum'})

        for person in person_list:
            channel.basic_publish(exchange='', routing_key=MQPublisher().topic, body=person.__str__())

        connection.close()


    @staticmethod
    def receive():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue='interpol_datas', durable=True, arguments={'x-queue-type': 'quorum'})

        def printer(ch, method, properties,body):
            cleaned_data = body.decode('utf-8').replace('\n', '').replace('\r', '')
            print(f" Mesaj Okundu: {cleaned_data}")

        channel.basic_consume(queue='interpol_datas',auto_ack=True,on_message_callback=printer)

        channel.start_consuming()

        channel.close()
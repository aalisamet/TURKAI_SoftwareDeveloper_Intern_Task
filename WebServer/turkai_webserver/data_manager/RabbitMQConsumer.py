import pika
from configuration.ConfigDistributor import ConfigDistributorService
class RabbitMQConsumer:

    def __init__(self):
        self.host = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","host")
        self.port = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","port")
        self.topic = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","topic")

    @staticmethod
    def receive():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQConsumer().host, port=RabbitMQConsumer().port))
        channel = connection.channel()
        channel.queue_declare(queue=RabbitMQConsumer().topic, durable=True, arguments={'x-queue-type': 'quorum'})

        def printer(ch, method, properties, body):
            cleaned_data = body.decode('utf-8').replace('\n', '').replace('\r', '')
            print(f" Mesaj Okundu: {cleaned_data}")

        channel.basic_consume(queue=RabbitMQConsumer().topic, auto_ack=True, on_message_callback=printer)

        channel.start_consuming()

        channel.close()
import pika
from configuration.ConfigDistributor import ConfigDistributorService
import ast

from notice_app.dto.WantedPersonDto import WantedPersonDto
from notice_app.services.WantedPersonManager import WantedPersonManager


class RabbitMQConsumer:

    def __init__(self):
        self.host = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","host")
        self.port = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","port")
        self.topic = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","topic")

    @staticmethod
    def consume():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQConsumer().host, port=RabbitMQConsumer().port))
        channel = connection.channel()
        channel.queue_declare(queue=RabbitMQConsumer().topic, durable=True, arguments={'x-queue-type': 'quorum'})

        def callback(ch, method, properties, body):
            cleaned_data_dict = ast.literal_eval(body.decode('utf-8').replace('\n', '').replace('\r', ''))
            person = WantedPersonDto(cleaned_data_dict)
            WantedPersonManager().add_wanted_person(person)

        channel.basic_consume(queue=RabbitMQConsumer().topic, auto_ack=True, on_message_callback=callback)

        channel.start_consuming()

        channel.close()
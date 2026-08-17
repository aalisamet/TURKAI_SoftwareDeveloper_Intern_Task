import ast
import asyncio

import aio_pika
from configuration.ConfigDistributor import ConfigDistributorService
import json

from notice_app.services.WantedPersonManager import WantedPersonManager


class RabbitMQConsumer:

    def __init__(self):
        self.host = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","host")
        self.port = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","port")
        self.topic = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","topic")

    @staticmethod
    async def callback(message: aio_pika.abc.AbstractIncomingMessage):
        message = ast.literal_eval(message.body.decode('utf-8').replace('\n', '').replace('\r', ''))
        data_dict = ast.literal_eval(message)
        print(type(data_dict))
        await WantedPersonManager.save_wanted_person(data_dict)





    @staticmethod
    async def consume():
        connection = await aio_pika.connect_robust(host=RabbitMQConsumer().host, port=RabbitMQConsumer().port)
        async with connection:
            channel = await connection.channel()
            print("Calisti 1")
            queue = await channel.declare_queue(name=RabbitMQConsumer().topic, arguments={'x-queue-type': 'quorum'}, durable=True)
            print("Calisti 2")
            await queue.consume(callback=RabbitMQConsumer.callback,no_ack=True)
            print("Calisti 3")
            try:
                await asyncio.Future()



            except asyncio.CancelledError as e:
                print(e.__str__())

'''

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

'''

import asyncio

import aio_pika
from configuration.ConfigDistributor import ConfigDistributorService
import json
from data_management.services.WantedPersonManager import WantedPersonManager



class RabbitMQConsumer:

    def __init__(self,wanted_person_manager:WantedPersonManager):
        self.host = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","host")
        self.port = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","port")
        self.topic = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","topic")
        self.pre_fetch_count = ConfigDistributorService.get_rabbitmq_config_data("RabbitMQ","pre_fetch_count")
        self.person_manager = wanted_person_manager



    async def callback(self,message: aio_pika.abc.AbstractIncomingMessage):
        try:
            data_dict =  json.loads(message.body.decode('utf-8').replace('\n', '').replace('\r', ''))
            print(data_dict)
            await self.person_manager.save_wanted_person(data_dict)
        except Exception as e:
            print(e.__str__())



    async def consume(self):
        while True:
            try:
                await asyncio.sleep(2)
                connection = await aio_pika.connect_robust(host=self.host, port=self.port)
                print("TASK 1")
                async with connection:
                    channel = await connection.channel()

                    print("TASK 2")
                    queue = await channel.declare_queue(name=self.topic, arguments={'x-queue-type': 'quorum'},durable=True)
                    await queue.consume(callback=self.callback,no_ack=True)
                    print("TASK 3")
                    try:
                        await asyncio.Future()
                    except asyncio.CancelledError as e:
                        print(e.__str__())
            except Exception as e:
                print(e.__str__() + "hatasi alindi baglanti 15 saniye sonra tekrar denenecek")
                await asyncio.sleep(15)





"""
ASGI config for turkai_webserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""


import os
import asyncio
from consumer.RabbitMQConsumer import RabbitMQConsumer
from data_management.services.UpdateDataService import UpdateDataService
from data_management.services.WantedPersonManager import WantedPersonManager
from django.core.asgi import get_asgi_application
from notice_app.websocket import WantedPersonWebSocket
from websockets.asyncio.server import serve
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turkai_webserver.settings')

turkai_webserver_asgi_app = get_asgi_application()






async def application(scope, receive, send):

    if scope['type'] == 'lifespan':
        consumer_task = None
        websocket = WantedPersonWebSocket()
        update_data = UpdateDataService(websocket)
        wanted_person_manager = WantedPersonManager()
        wanted_person_manager.register_new_data_observer(update_data)
        wanted_person_manager.register_update_observer(update_data)
        rabbitmq_consumer = RabbitMQConsumer(wanted_person_manager)
        websocket_server = await serve(handler=websocket.handler, host=websocket.host, port=websocket.port)

        while True:
            message = await receive()

            if message['type'] == 'lifespan.startup':

                consumer_task = asyncio.create_task(rabbitmq_consumer.consume())
                await send({'type': 'lifespan.startup.complete'})

            elif message['type'] == 'lifespan.shutdown':

                await websocket.shutdown()
                websocket_server.close()
                await websocket_server.wait_closed()

                if consumer_task and not consumer_task.done():
                    consumer_task.cancel()

                    try:
                        await consumer_task
                    except asyncio.CancelledError:
                        pass
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:

        await turkai_webserver_asgi_app(scope, receive, send)








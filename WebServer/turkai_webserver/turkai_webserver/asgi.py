"""
ASGI config for turkai_webserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""


import os
import asyncio
from channels.routing import ProtocolTypeRouter,URLRouter

from consumer.RabbitMQConsumer import RabbitMQConsumer
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from data_management.services.WantedPersonManager import WantedPersonManager
from notice_app.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turkai_webserver.settings')

turkai_webserver_asgi_app = get_asgi_application()

turkai_webserver_application = ProtocolTypeRouter(
    {
        "http": turkai_webserver_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

async def application(scope, receive, send):

    if scope['type'] == 'lifespan':
        consumer_task = None
        rabbitmq_consumer = RabbitMQConsumer(WantedPersonManager())
        while True:
            message = await receive()

            if message['type'] == 'lifespan.startup':

                consumer_task = asyncio.create_task(rabbitmq_consumer.consume())
                await send({'type': 'lifespan.startup.complete'})

            elif message['type'] == 'lifespan.shutdown':
                if consumer_task and not consumer_task.done():
                    consumer_task.cancel()
                    try:
                        await consumer_task
                    except asyncio.CancelledError:
                        pass
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:

        await turkai_webserver_application(scope, receive, send)

async def consume_rabbitmq():
    rabbitmq_consumer = RabbitMQConsumer(WantedPersonManager())
    print("Hello World")
    while True:
        task = asyncio.create_task(rabbitmq_consumer.consume())
        await task
        await asyncio.sleep(1)
consume_rabbitmq()






'''
async def worker():
    print("[Worker] Arka plan servisi başlatıldı.")
    try:
        while True:
            # Yapılacak asenkron işlem
            # await consumer.consume() gibi
            print("[Worker] Görev çalışıyor...")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("[Worker] Kapatma sinyali alındı, temizlik yapılıyor...")
    except Exception as e:
        print(f"[Worker] Hata: {e}")
'''




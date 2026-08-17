"""
ASGI config for turkai_webserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
import asyncio
from django.core.asgi import get_asgi_application

from consumer.RabbitMQConsumer import RabbitMQConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turkai_webserver.settings')

django_app = get_asgi_application()


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


# 3. Lifespan destekli özel ASGI sarmalayıcısı (wrapper)
async def application(scope, receive, send):
    if scope['type'] == 'lifespan':
        consumer_task = None
        while True:
            message = await receive()

            # Sunucu ayağa kalkarken
            if message['type'] == 'lifespan.startup':

                consumer_task = asyncio.create_task(RabbitMQConsumer.consume())
                await send({'type': 'lifespan.startup.complete'})

            # Sunucu kapanırken
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
        # HTTP / WebSocket isteklerini doğrudan Django'ya yönlendir
        await django_app(scope, receive, send)



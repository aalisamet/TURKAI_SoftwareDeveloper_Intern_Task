from typing import override

from data_management.services.Observer import Observer, DataEventType
from notice_app.websocket_consumer import WebsocketConsumer

class UpdateDataService(Observer):




    @override
    async def update(self,data_event):

            match data_event.event_type:
                case DataEventType.CREATED:
                    WebsocketConsumer().receive("deneme")

                case DataEventType.UPDATED:
                    WebsocketConsumer().receive("deneme2")


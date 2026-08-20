from typing import override
from data_management.services.Observer import Observer, DataEventType
from notice_app.websocket import WantedPersonWebSocket

class UpdateDataService(Observer):

    def __init__(self,websocket):
        self.websocket=websocket


    @override
    async def update(self,data_event):
            match data_event.event_type:
                case DataEventType.CREATED:
                    await self.websocket.data_created(data_event.data.convert_json())
                case DataEventType.UPDATED:
                    await self.websocket.data_updated(data_event.data.convert_json())


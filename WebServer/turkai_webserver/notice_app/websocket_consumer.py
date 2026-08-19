import json
from channels.generic.websocket import AsyncWebsocketConsumer
from data_management.services import Observer

class PersonDataConsumer(AsyncWebsocketConsumer):
    group_name= "interpol_data_stream"
    async def connect(self):


        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self,code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        # Receive message from WebSocket

    async def stream_red_notices(self,red_notice_list):
        text_data_json = json.loads(red_notice_list)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "message": message}
        )

        # Receive message from room group



    async def broadcast_person_event(self, event:Observer.DataEvent):
        await self.send(text_data=json.dumps({
            "event_type": event.event_type.__str__(),
            "data": event.data
        }))

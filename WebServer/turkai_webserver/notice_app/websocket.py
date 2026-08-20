import asyncio

from websockets.asyncio.server import broadcast
class WantedPersonWebSocket:

    def __init__(self):
        self.port = 8080
        self.host = "localhost"
        self.subscribers = set()

    async def handler(self,websocket):
        self.subscribers.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.subscribers.remove(websocket)

    async def data_created(self,data):
        print("it works fine")
        try:
            broadcast(self.subscribers, data)
            print("it works fine two")
        except Exception as e:
            print(e.__str__()+"Baglanti sirasinda hata olustu")


    async def data_updated(self,data):
        print("it works fine")
        try:
            broadcast(self.subscribers, data)
            print("it works fine two")
        except Exception as e:
            print(e.__str__()+"Baglanti sirasinda hata olustu")

    async def shutdown(self):
        for sub in self.subscribers:
            try:
                await sub.close(reason="Server shutting down")
            except Exception as e:
                print(e.__str__())
                pass
            self.subscribers.clear()

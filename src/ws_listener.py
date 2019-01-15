import websockets
import asyncio
from . import Callback

class WSListener(Callback):

    ws_url = ""

    def __init__(self, ws_url="", logger=None):
        super().__init__("WSS", logger=logger)
        self.ws_url = ws_url

    async def run(self):
        try:
            self.logger.warning("APP STARTED! GOING TO LISTEN %s" % self.ws_url)
            counter = 0
            async with websockets.connect(self.ws_url) as socket:
                while True:
                    message = await socket.recv()
                    tasks = [
                        cb.callback(message) for cb in self.callbackList
                    ]
                    await asyncio.wait(tasks)
        except Exception as e:
            self.logger.exception(e)

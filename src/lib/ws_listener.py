import websockets
import asyncio
from callback import Callback

class WSListener(Callback):

    def __init__(self, ws_url, sleep_ms=30000, command_list=[]):
        super().__init__("WSS")
        self.ws_url = ws_url
        self.command_list = command_list
        self.sleep_ms = int(sleep_ms)

    async def run(self):
        self.logger.warning("APP STARTED! GOING TO LISTEN %s" % self.ws_url)
        while True:
            try:
                async with websockets.connect(self.ws_url) as socket:
                    self.logger.warning("successfully connected to %s" % self.ws_url)

                    #send messages if any supplied
                    for cmd in self.command_list:
                        self.logger.warning("sending message: %s" % cmd)
                        await socket.send(cmd)

                    while True:
                        message = await socket.recv()
                        #self.logger.info("got message %s" % message)
                        # tasks = [
                        #     cb.callback(message) for cb in self.callbackList
                        # ]
                        # await asyncio.wait(tasks)
                        await self.sendCallback(message)
            except Exception as e:
                self.logger.exception("error while performing listen to websocket %s" % self.ws_url)
                self.logger.exception(e)
                self.logger.exception("going for a sleep to %sms" % self.sleep_ms)
                await asyncio.sleep(self.sleep_ms / 1000)

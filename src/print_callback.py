from . import Callback
import asyncio

class PrintCallback(Callback):

    def __init__(self):
        super().__init__("PrintCallback")

    async def processCallback(self, obj):
        print (str(obj))

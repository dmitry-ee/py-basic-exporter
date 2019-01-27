import asyncio
from callback import Callback
from datetime import datetime

class BasicCallRepeater(Callback):

    def __init__(self, sleep_ms=60000, api=None, repeat_lambda=None):
        super().__init__(self.__class__.__name__)

        self.sleep_seconds = int(sleep_ms)/1000
        self.api = api
        self.repeat_lambda = repeat_lambda

    async def run(self):
        self.logger.warning("BasicCallRepeater started!")

        if not callable(self.repeat_lambda):
            raise Exception("repeat_lambda is not properly supplied!")

        while True:

            try:

                call_result = self.repeat_lambda(self)
                if call_result != None:
                    await self.sendCallback(call_result)

            except Exception as e:
                self.logger.exception("Caught exception %s" % e)

            # data retrieving
            # TODO: call something in the lambda supplied within __init__
            #
            # for ccap_info in filtered_ccap:
            #     await self.sendCallback(ccap_info)
            # await self.sendCallback(global_cap)

            await asyncio.sleep(self.sleep_seconds)

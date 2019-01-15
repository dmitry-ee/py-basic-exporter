import asyncio
import random
from . import Callback
from . import Tick
import prowlpy
import functools

class Prowl(Callback):
    api_key         = None
    prowl_api       = None
    alert_priority  = None
    api_initialized = False
    alert_level_1   = 0
    alert_level_2   = None

    def __init__(self, app_name, api_key, alert_level_1=0, alert_level_2=None):
        super().__init__("Prowl", objectType=Tick)
        self.api_key            = api_key
        self.app_name           = app_name
        self.api_initialized    = False
        self.alert_level_1      = float(alert_level_1)
        self.alert_level_2      = float(alert_level_2)
        self._initProwlApi()

    def _initProwlApi(self):
        try:
            self.prowl_api = prowlpy.Prowl(self.api_key)
            #verify        = self.prowlApi.verify_key(self.apiKey)
            #keyInfo = self.prowlApi.retrieve_apikey(self.providerKey)
            self.logger.warn("Connected to Prowl API: %s with key=%s and app_name=%s" % (self.prowl_api, self.api_key, self.app_name))
            self.api_initialized = True
        except Exception as e:
            #print("Prowl Connection error: %s" % e)
            self.logger.exception(e)

    async def processCallback(self, obj):
        if not self.api_initialized:
            return
        try:
            #await asyncio.sleep(random.randint(1000,5000) * 0.001)
            alert_level = self._get_alert_priority(obj)
            if alert_level is not None:
                event, description = self._formatMessage(obj, alert_level)
                await self.eventLoop.run_in_executor(None, functools.partial(
                    self.prowl_api.post,
                    application = self.app_name,
                    event       = event,
                    priority    = alert_level,
                    description = description,
                ))
                #await self.prowlApi.post(application=self.appName, event=event, description=description)
                self.logger.warn("%s: [%s] sending tick %s!" % ( self.name, alert_level, obj ) )
            else:
                self.logger.info("%s: skipping tick with amount %s" % ( self.name, obj.amount ) )
        except Exception as e:
            self.logger.exception("ProwlAPI post exception: %s" % e)

    def _get_alert_priority(self, tick):
        if self.alert_level_2 and self.alert_level_2 < self.alert_level_1:
            self.logger.exception("alert_level_2 = %s should be greater than alert_level_1 = %s" % ( self.alert_level_2, self.alert_level_1 ))
            return None

        if self.alert_level_2 and self.alert_level_2 >= 0 and tick.amount >= self.alert_level_2:
            return 2

        if self.alert_level_1 and self.alert_level_1 >= 0 and tick.amount >= self.alert_level_1:
            return 1

        return None

    def _formatMessage(self, tick, alert_level):
        obj = tick.represent()
        huge_msg = "HUGE" if alert_level == 2 else "BIG"
        event_name = "%s [%s] %s %s" % ( obj["deal"].upper(), obj["short_ts"], obj["exchange"].upper(), huge_msg )
        s1 = obj.get("symbol1")
        s2 = obj.get("symbol2")
        amount1 = obj[s1+"_b"]
        amount2 = obj[s2+"_b"]
        message = "%s=%s / %s=%s by %s" % ( s1.upper(), amount1, s2.upper(), amount2, obj["price"] )
        return event_name, message

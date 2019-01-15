# imports
import logging
import sys
import os
import json_log_formatter
import ujson
import configparser
import asyncio
# ##

# logging settings
LOGGER = logging.getLogger()

if "LOG_LEVEL" in os.environ:
    LOGGER.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL")))
    LOGGER.warn("setting log level to %s" % os.environ.get("LOG_LEVEL"))
else:
    LOGGER.setLevel(logging.WARN)

handler = logging.StreamHandler(sys.stdout)
#handler.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))
formatter = json_log_formatter.JSONFormatter()
formatter.json_lib = ujson
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

LOGGER.info("LOGGER INITIALIZED")
# ##

# config settings
CONFIG = configparser.ConfigParser()
CONFIG.read("config.yml")
print(CONFIG.__dict__)
# ##

try:
    from app import App

    application = App()

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(application.run())

except Exception as e:
    LOGGER.exception(e)

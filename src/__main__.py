# imports
import logging, sys, os, json_log_formatter, ujson, asyncio, yaml, flatten_dict
from munch import Munch

import importdir
importdir.do("lib", globals())
# ##

# logging settings
LOGGER = logging.getLogger()

if "LOG_LEVEL" in os.environ:
    LOGGER.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL")))
    LOGGER.warning("setting log level to %s" % os.environ.get("LOG_LEVEL"))
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
def underscore_reducer(k1, k2):
    if k1 is None:
       return k2.upper().replace(".", "_")
    else:
       return (k1 + "_" + k2).upper().replace(".", "_")

def underscore_splitter(flat_key):
    return flat_key.lower().split("_")


try:
    with open("config.yml", 'r') as ymlfile:
        CONFIG = flatten_dict.flatten(yaml.load(ymlfile, Loader=yaml.SafeLoader), reducer=underscore_reducer)
    LOGGER.warning("got default config: %s" % CONFIG)
    if len(os.environ) != 0:
        #LOGGER.warning("overriding default config with ENV")
        for env_var in os.environ:
            CONFIG[env_var] = os.environ.get(env_var)
        LOGGER.warning("result config: %s" % CONFIG)

except Exception as e:
    LOGGER.warning(e)
    LOGGER.warning("using empty config")
    CONFIG = {}
# ##

try:

    import app

    CONFIG = Munch.fromDict(flatten_dict.unflatten(CONFIG, splitter=underscore_splitter))

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.run(CONFIG))

except Exception as e:
    LOGGER.exception(e)

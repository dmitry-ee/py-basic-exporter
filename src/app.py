import logging

class App():
    def __init__(self):
        self.logger = logging.getLogger()

    async def run(self):
        self.logger.warn("APP:run")

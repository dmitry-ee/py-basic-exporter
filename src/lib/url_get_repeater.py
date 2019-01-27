import requests
from datetime import datetime
from basic_call_repeater import BasicCallRepeater

class UrlGetRepeater(BasicCallRepeater):
    # url to call every sleep_ms
    # output_type could be `json` or `text`
    def __init__(self, url, output_type="json", sleep_ms=60000, headers={}):
        super().__init__(
            sleep_ms=sleep_ms,
            repeat_lambda=lambda self: self.get(url),
            repeater_name=self.__class__.__name__ + ":" + url
        )
        self.headers = headers
        self.output_type = output_type
        self.logger.info("default headers: %s" % str(headers))

    def get(self, url):
        self.logger.info("performing GET request to %s" % url)
        if len(self.headers) == 0:
            get_result = requests.get(url)
        else
            get_result = requests.get(url, headers=self.headers)
        if self.output_type == "json":
            return get_result.json()
        # more repetitions of if (if necessary)
        else:
            return get_result.text

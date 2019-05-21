import requests
from datetime import datetime
from basic_call_repeater import BasicCallRepeater

class UrlsGetRepeater(BasicCallRepeater):
    # url to call every sleep_ms
    # output_type could be `json` or `text`
    def __init__(self, urls, output_type="json", sleep_ms=60000, headers={}):
        super().__init__(
            sleep_ms=sleep_ms,
            repeat_lambda=lambda self: self.get_many(urls),
            repeater_name=self.__class__.__name__ + ":" + str(urls)
        )
        self.headers = headers
        self.output_type = output_type
        self.logger.info("default headers: %s" % str(headers))

    def get_many(self, urls):
        responses = [self.get(url) for url in urls]
        return responses

    def get(self, url):
        self.logger.info("performing GET request to %s" % url)
        if len(self.headers) == 0:
            get_result = requests.get(url)
        else:
            get_result = requests.get(url, headers=self.headers)
        if self.output_type == "json":
            return get_result.json()
        # more repetitions of if (if necessary)
        else:
            return get_result.text

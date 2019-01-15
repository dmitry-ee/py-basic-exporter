import json
import datetime

class Tick(object):
    exchange    = None
    timestamp   = None
    price       = None
    deal        = None
    symbol1     = None
    symbol2     = None
    pair        = None

    valid       = False

    def __init__(self, exchange, timestamp, price, amount, deal, symbol1, symbol2):
        self.valid      = False
        self.exchange   = exchange
        self.timestamp  = float(timestamp)
        self.price      = float(price)
        self.deal       = deal.lower()
        self.symbol1    = symbol1.lower()
        self.symbol2    = symbol2.lower()
        self.amount     = amount
        setattr(self, self.symbol1, amount)
        setattr(self, self.symbol2, amount * self.price)
        self.pair = ("%s%s" % ( symbol1, symbol2 ) ).upper()

        self.valid      = True

    def __str__(self):
        return "{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}".format(self.pair, self.exchange, self.timestamp, self.price, getattr(self, self.symbol1), getattr(self, self.symbol2), self.deal)

    def represent(self):
        result = {}
        result["exchange"]      = self.exchange
        result["timestamp"]     = datetime.datetime.utcfromtimestamp(self.timestamp / 1000.0)
        result["short_ts"]      = datetime.datetime.utcfromtimestamp(self.timestamp / 1000.0).strftime("%d %H:%M")
        result["price"]         = round(self.price, 2) if self.symbol2 == "usd" else round(self.price, 8)
        result["price_b"]       = self._format_value(self.price)
        result[self.symbol1]    = getattr(self, self.symbol1) #round(getattr(self, self.symbol1), 8)
        result[self.symbol2]    = getattr(self, self.symbol2) #round(getattr(self, self.symbol2), 0) if self.symbol2 == "usd" else round(getattr(self, self.symbol2), 8)
        result["symbol1-ama"]   = getattr(self, self.symbol1)
        result["symbol2-ama"]   = getattr(self, self.symbol2)
        result[self.symbol1+"_b"] = self._format_value(getattr(self, self.symbol1))
        result[self.symbol2+"_b"] = self._format_value(getattr(self, self.symbol2))
        result["pair"]          = self.pair
        result["deal"]          = self.deal
        result["symbol1"]       = self.symbol1
        result["symbol2"]       = self.symbol2
        return result

    def _format_value(self, val):
        if val > 1000000:
            return "%sM" % round(val/1000000, 3)
        if val > 10000:
            return "%sK" % round(val/1000, 3)
        if val > 10:
            return int(round(val, 0))
        return round(val, 8)

    def to_json(self):
        repr = self.represent()
        repr["timestamp"] = repr["timestamp"].timestamp()
        return json.dumps(repr)

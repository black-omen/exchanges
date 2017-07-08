from collections.abc import Sequence

from .assets import Asset

class Order(object):
    """This class represents an order than can be plased on an exchange. 
       
       If a price is not given, then the Order represents a BUY/SELL at
       market price.

       If the validate flag is present, then the order is only validated and
       not placed in the market"""
    PENDING = -1
    OPEN = 0
    CLOSED = 1
    CANCELED = 2
    EXPIRED = 3

    BUY='buy'
    SELL='sell'

    def __init__(self, action, asset_pair, volume, price=None, validate=False):
        if action not in [Order.BUY, Order.SELL]:
            raise ValueError("Action must be Order.BUY or Order.SELL")

        if not isinstance(asset_pair, Sequence) or len(asset_pair) != 2:
            raise TypeError("asset_pair must be a sequence of lenght 2")

        if any([not isinstance(a, Asset) for a in asset_pair]):
            raise TypeError("asset_pair must be a sequence of assets, "
                            "not {}, {}".format(*map(type, asset_pair)))
        if volume < 0:
            raise ValueError("volume should be strictly positive")

        self.id = None
        self._action = action
        self._asset_pair = asset_pair
        self._volume = volume
        self._price = price
        self.status = None
        self.time_placed = None
        self.closed_price = None
        self.closed_time = None
        self._validate = validate

    @property
    def action(self):
        return self._action

    @property
    def asset_pair(self):
        return self._asset_pair

    @property
    def volume(self):
        return self._volume

    @property
    def price(self):
        return self._price

    @property
    def validate(self):
        return self._validate

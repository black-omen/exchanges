from abc import ABC, abstractmethod
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PRIVATE_DATA_DIR = os.path.join(DATA_DIR, 'private')


class Balance(object):
    """TODO: Check types"""
    def __init__(self, asset, amount=0):
        self._asset = asset
        self._amount = amount

    @property
    def asset(self):
        return self._asset

    @property
    def amount(self):
        return self._amount


class Exchange(ABC):
    """This class defines the minimum set of methods to interact
        with an Exchanges"""

    @abstractmethod
    def server_time(self):
        """Queries the current server time"""
        pass

    @abstractmethod
    def latest_trade(self, asset_pair):
        """Retrieves the latest trade made on the supplied asset"""
        pass

    @abstractmethod
    def place_order(self, order):
        """Places an order in the exchange"""
        pass

    @abstractmethod
    def order_info(self, order_id):
        """Retrieves information about an order"""
        pass

    @abstractmethod
    def trades_history(self, asset_pair, start_time, finish_time):
        """Retrieves the trades made between the supplied time interval"""
        pass


class OrderInformation(object):
    """TODO: Check types"""
    def __init__(self, status):
        self._status = status

    @property
    def status(self):
        return self._status


class Trade(object):
    """TODO: Check types"""
    def __init__(self, asset_pair, price, volume):
        self._asset_pair = asset_pair
        self._price = price
        self._volume = volume

    @property
    def asset_pair(self):
        return self._asset_pair

    @property
    def price(self):
        return self._price

    @property
    def volume(self):
        return self._volume

from .kraken import Kraken

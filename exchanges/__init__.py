from abc import ABC, abstractmethod


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

from .kraken import Kraken

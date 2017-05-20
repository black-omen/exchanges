import requests

from exchanges import Exchange


class Kraken(Exchange):

    def __init__(self):
        self.timeout = 5.0
        self.url = 'https://api.kraken.com/0/'

    def server_time(self):
        """Queries the current server time (unix time stamp)"""
        return self._public_query('Time')['unixtime']

    def latest_trade(self, asset_pair):
        pass

    def place_order(self, order):
        pass

    def order_info(self, order_id):
        pass

    def trades_history(self, asset_pair, start_time, finish_time):
        pass

    def _public_query(self, query_name, parameters=None):
        """Queries public data on Kraken"""

        # Request public data. This can raise an exception
        # if there is a connection error or if the request times
        # out. In addition, raise an exception if the status is not
        # OK.
        url = '{}public/{}'.format(self.url, query_name)
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()

        return response.json()['result']

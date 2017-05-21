import base64
import hashlib
import hmac
import os
import requests
import time
import urllib.parse

from exchanges import Exchange, OrderInformation, PRIVATE_DATA_DIR, Trade


class Kraken(Exchange):

    def __init__(self):
        self.timeout = 5.0
        self.url = 'https://api.kraken.com/0/'

        # Load the API keys from the data folder.
        key_file = os.path.join(PRIVATE_DATA_DIR, 'kraken-key')
        if os.path.exists(key_file):
            with open(key_file, 'rt') as f:
                self.public_key = f.readline().rstrip()
                self.private_key = f.readline().rstrip()
        else:
            raise Warning('The Kraken API requires an API key to access '
                          'private user data. Please add your public '
                          'and private keys to the file '
                          '\'exchanges/data/private/kraken-key\'.')
            self.public_key = None
            self.privage_key = None

    def server_time(self):
        """Queries the current server time (unix time stamp)"""

        return self._public_query('Time')['unixtime']

    def latest_trade(self, asset_pair):
        """Queries the latest trade"""

        ticker = self._public_query('Ticker', {'pair': [asset_pair]})
        price, volume = ticker[asset_pair]['c']

        return Trade(asset_pair, price, volume)

    def place_order(self, order):
        pass

    def order_info(self, order_id):
        """Queries information about an order"""

        info = self._private_query('QueryOrders', {'txid': order_id})
        order_info = OrderInformation(info[order_id]['status'])

        return order_info

    def trades_history(self, asset_pair, start_time, finish_time):
        pass

    def _private_query(self, query_name, data=None):
        """Queries private data on Kraken"""

        if self.public_key is None or self.private_key is None:
            raise ValueError('Querying the private user '
                             'data requires an API key.')

        nonce = int(1000 * time.time())

        url = '{}private/{}'.format(self.url, query_name)
        uri = '/0/private/{}'.format(query_name)

        if data is None:
            data = {}
        data['nonce'] = nonce

        # Encode the POST data using Kraken's scheme.
        post_data = urllib.parse.urlencode(data)
        data_nonce = (str(nonce) + post_data).encode()
        message = uri.encode() + hashlib.sha256(data_nonce).digest()
        signature = hmac.new(base64.b64decode(self.private_key), message,
                             hashlib.sha512)
        signature_digest = base64.b64encode(signature.digest()).decode()

        # Request private data. This can raise an exception
        # if there is a connection error or if the request times
        # out. In addition, raise an exception if the status is not
        # OK.
        headers = {'API-Key': self.public_key, 'API-Sign': signature_digest}
        response = requests.post(url, headers=headers, data=post_data,
                                 timeout=self.timeout)
        response.raise_for_status()

        json = response.json()

        if len(json['error']) > 0:
            raise RuntimeError(json['error'][0])

        return json['result']

    def _public_query(self, query_name, parameters=None):
        """Queries public data on Kraken"""

        # Request public data. This can raise an exception
        # if there is a connection error or if the request times
        # out. In addition, raise an exception if the status is not
        # OK.
        url = '{}public/{}'.format(self.url, query_name)
        response = requests.get(url, params=parameters, timeout=self.timeout)
        response.raise_for_status()

        json = response.json()

        if len(json['error']) > 0:
            raise RuntimeError(json['error'][0])

        return json['result']

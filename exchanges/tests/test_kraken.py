import os
import time
import unittest

from requests.exceptions import Timeout, HTTPError

from exchanges import DATA_DIR, Kraken, OrderInformation, Trade


class TestKraken(unittest.TestCase):
    """Tests for the exchanges.Kraken class"""

    def test_order_info(self):
        """Test the order_info method"""

        kraken = Kraken()

        # Get a closed order id.
        closed_order_file = os.path.join(DATA_DIR, 'kraken', 'closed-order-id')
        if os.path.exists(closed_order_file):
            with open(closed_order_file) as f:
                order_id = f.readline().rstrip()
        else:
            raise IOError('Testing the order_info method requires an order '
                          'id. Plead add a closed order id to the file '
                          '\'exchanges/data/kraken/closed-order-id\'.')

        # If the API keys are not set, we cannot query
        # private user data.
        key = kraken.public_key
        kraken.public_key = None
        self.assertRaises(ValueError, kraken.order_info, order_id)
        kraken.public_key = key
        time.sleep(3)

        # Get the information about some order. Verify that the
        # status is closed.
        # TODO: More in depth validation once we define what an
        # OrderInformation should contain.
        order_info = kraken.order_info(order_id)
        self.assertTrue(isinstance(order_info, OrderInformation))
        self.assertEqual(order_info.status, 'closed')
        time.sleep(3)

    def test_server_time(self):
        """Test the server_time method"""

        # On a normal query, the time should be close to the
        # current time. There is a lot of jitter on the time
        # returned by the server, so we judge that a
        # difference of 1 minute is ok.
        kraken = Kraken()
        server_time = kraken.server_time()
        current_time = time.time()
        self.assertTrue(abs(server_time - current_time) < 60)

        time.sleep(3)

        # Set the timeout limit to a very low value to be
        # sure it is raised.
        kraken.timeout = 1e-16
        self.assertRaises(Timeout, kraken.server_time)
        kraken.timeout = 5.0

        time.sleep(3)

        # Change the url to get and HTTP error.
        kraken.url = kraken.url[:-1]
        self.assertRaises(HTTPError, kraken.server_time)

    def test_latest_ticker(self):
        """Test the latest_ticker method"""

        kraken = Kraken()

        # Get the latest trade. I cannot find a way to validate
        # the result, so I just assume that if it returns a
        # trade everything is ok.
        trade = kraken.latest_trade('XETHZEUR')
        self.assertTrue(isinstance(trade, Trade))

        time.sleep(3)

        # Querying a non existent asset pair should fail.
        self.assertRaises(RuntimeError, lambda: kraken.latest_trade('FAKE'))

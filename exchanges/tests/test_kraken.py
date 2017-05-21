import time
import unittest

from requests.exceptions import Timeout, HTTPError

from exchanges import Kraken, Trade


class TestKraken(unittest.TestCase):
    """Tests for the exchanges.Kraken class"""

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


    def test_trades_history(self):
        """Test the trades_history method"""

        kraken = Kraken()

        asset = 'XXBTZEUR'
        since = 1470092400  # 2016-08-02 01:00:00 - unix timestamp
        trades_history = kraken.trades_history(asset, since)

        # The first was filled shortly after 'since'
        tolerance = 10  # 10ms in unix timestamp
        self.assertTrue(trades_history[0].time - since < tolerance)
        self.assertEqual(len(trades_history), 1000)

        # The rest are ordered
        for i, trade in enumerate(trades_history[1:], 1):
            self.assertTrue(trade.time > trades_history[i-1].time)

        # By looking at /Trades?pair=XXBTZEUR&since=1470092400000000000
        # in a web browser we can create a specific test with only
        # 3 orders between 'since' and 'until'
        until = 1470092421.1177
        gt_prices_volumes = [(538.05000, 1.07597000) ,(538.05000, 0.00020000),
                             (538.05000, 0.05610236)]
        trades_history = kraken.trades_history(asset, since, until)
        for i, trade in enumerate(trades_history):
            self.assertEqual(trade.asset_pair, asset)
            self.assertEqual(trade.price, gt_prices_volumes[i][0])
            self.assertEqual(trade.volume, gt_prices_volumes[i][1])

        until = 1470150000 # 16hs of diff.
        trades_history = kraken.trades_history(asset, since, until)

        # First and last within boundaries
        self.assertTrue(len(trades_history) > 1000)
        self.assertTrue(trades_history[0].time - since < tolerance)
        self.assertTrue(until - trades_history[-1].time < tolerance)

        # The rest are ordered
        for i, trade in enumerate(trades_history[1:], 1):
            self.assertTrue(trade.time > trades_history[i-1].time)

        time.sleep(1)

        # Querying a non existent asset pair should fail.
        self.assertRaises(RuntimeError, lambda: kraken.trades_history('FAKE',
                                                                      123456))

import time
import unittest

from requests.exceptions import Timeout, HTTPError

from exchanges import Kraken


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
        kraken.timeout = 1.0

        time.sleep(3)

        # Change the url to get and HTTP error.
        kraken.url = kraken.url[:-1]
        self.assertRaises(HTTPError, kraken.server_time)

class Asset(object):

    def __init__(self, name, atype, iso4217_a3=None, abbreviation=None):

        if iso4217_a3 is None and abbreviation is None:
            raise ValueError('At least one denomination is needed')

        if atype not in ['X', 'Z']:
            raise ValueError("atype must be either 'X' or 'Z'")

        self._name = name
        self._iso4217_a3 = iso4217_a3
        self._abbreviation = abbreviation
        self._atype = atype

    @property
    def name(self):
        return self._name

    @property
    def iso4217_a3(self):
        return self._iso4217_a3

    @property
    def abbreviation(self):
        return self._abbreviation

    @property
    def code(self):
        if self.iso4217_a3:
            return self._atype + self._iso4217_a3
        else:
            return self._atype + self._abbreviation

    @property
    def atype(self):
        return self._atype


# Cryptocurrencies
Bitcoin = Asset('bitcoin', 'X', 'BTC', 'BTC')
Ethereum = Asset('ethereum', 'X', 'ETH', 'BTC')
Litecoin = Asset('litecoin', 'X', 'LTC', 'LTC')
Ripple = Asset('ripple', 'X', 'XRP', 'XRP')
Zcoin = Asset('zcoin', 'X', None, 'ZEC')

# Currencies
Euro = Asset('euro', 'Z', 'EUR', 'EUR')
Dolar = Asset('dolar', 'Z', 'USD', 'USD')

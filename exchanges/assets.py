class Asset(object):

    CRYPTO='X'
    FIAT='Z'

    def __init__(self, name, atype, iso4217_a3=None, abbreviation=None):

        if iso4217_a3 is None and abbreviation is None:
            raise ValueError('You must provided either an abbreviation or '
                             'the iso4217_a3 name')

        if atype not in [Asset.CRYPTO, Asset.FIAT]:
            raise ValueError("atype must be either {} or {}"
                             .format(Asset.CRYPTO, Asset.FIAT))

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

    def __str__(self):
        if self.iso4217_a3:
            return self._atype + self._iso4217_a3
        else:
            return self._atype + self._abbreviation

    @property
    def atype(self):
        return self._atype


# Cryptocurrencies
Bitcoin = Asset('bitcoin', Asset.CRYPTO, 'BTC', 'BTC')
Ethereum = Asset('ethereum', Asset.CRYPTO, 'ETH', 'BTC')
Litecoin = Asset('litecoin', Asset.CRYPTO, 'LTC', 'LTC')
Ripple = Asset('ripple', Asset.CRYPTO, 'XRP', 'XRP')
Zcoin = Asset('zcoin', Asset.CRYPTO, None, 'ZEC')

# Currencies
Euro = Asset('euro', Asset.FIAT, 'EUR', 'EUR')
Dollar = Asset('dollar', Asset.FIAT, 'USD', 'USD')

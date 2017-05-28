from .assets import Asset

def basic_order_check(action, asset_pair):
    if action not in ['buy', 'sell']:
        raise ValueError("Action must be 'buy' or 'sell'")

    asset0, asset1 = asset_pair
    if not isinstance(asset0, Asset) or not isinstance(asset1, Asset):
        raise ValueError("Not recognized asset pair")


class Order(object):
    """This is the simplest type of order, given an action (i.e. BUY/SELL);
       an assets_pair (A0, A1) and a volume, it represents:

       BUY/SELL `volume` of A0 using/for some volume of A1, which follows the
       relationship: volume(A0)*price = volume(A1). Where `price` is dictated
       by the market

       Examples
       --------
       Order(action:BUY, asset_pair:(ETH, BTC), volume:1.5) means:
       "BUY 1.5 Ethereum using as much Bitcoin as the market dictates"

       Order(action:SELL, asset_pair:(Bitcoin, Ethereum), volume:1.5) means:
       'SELL 1.5 Ethereum for the amount of Bitcoin the market dictates'"""
    def __init__(self, action, asset_pair, volume,
                 leverage=None, only_validate=False):
        basic_order_check(action, asset_pair)
        self._action = action
        self._asset_pair = asset_pair
        self._volume = volume
        self._leverage = leverage
        self._validate = only_validate

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
    def leverage(self):
        return self._leverage

    @property
    def validate(self):
        return self._validate


class Limit(Order):
    """It's like an order, but it allows to set the desired exchange price.
       Given an action (i.e. BUY/SELL); an assets_pair (A0, A1); a volume and
       a limit_price, it represents:

       BUY/SELL `volume` of A0 using/for some volume of A1, which follows the
       relationship: volume(A0)*limit_price = volume(A1).

       Examples
       --------
       Limit(action:BUY, asset_pair:(ETH, BTC), volume:1.5, limit_price:0.07)
       means: "BUY 1.5 Ethereum for the price of 0.07 Bitcoin per unit of
               Ethereum. This is, 0.105 Bitcoins"

       Limit(action:SELL, asset_pair:(ETH, BTC), volume:1.5, limit_price:0.07)
       means: "SELL 1.5 Ethereum for the price of 0.07 Bitcoin per unit of
               Ethereum. This is, 0.105 Bitcoin """

    def __init__(self, action, asset_pair, volume, limit_price,
                 leverage=None, only_validate=False):
        Order.__init__(self, action, asset_pair, volume,
                       leverage, only_validate)
        self._limit = limit_price

    @property
    def limit(self):
        return self._limit


class TrailingStop(Order):
    """Triggers a market order (BUY or SELL) when the market price reaches
       a desired offset.

       Given an asset_pair (A0, A1) and a volume:

       - For the action BUY, and a STRICTLY POSITIVE offset, this Order will
         start following the market price and keep record of the MINIMUM price
         achieved SINCE this order was placed. If at some point, the market
         price goes OVER the minimum price by the desired offset, then an
         Order(BUY, (A0, A1), volume) will be triggered.

       - For the action SELL, and a STRICTLY NEGATIVE offset, this Order will
         start following the market price and keep record of the MAXIMUM price
         achieved SINCE this order was placed. If at some point, the market
         price goes UNDER the maximum price by the desired offset, then an
         Order(BUY, (A0, A1), volume) will be triggered.

      The offset can be relative to the current market price.

      Examples
      --------
      For these examples, let's asume that the market price when placing this
      order was: ETH = 0.07 BTC.

      TrailingStop(action:BUY, asset_pair:(ETH, BTC), volume:1.5, offset:+5,
                   relative:True)
      means: "The minimum is ETH = 0.07 BTC. Keep track of the market and go
              recording the minimum price achieved. If at some point the
              market price goes UP by a 5% respect to the minimum, then place
              the Order(BUY, (ETH, BTC), 1.5)"

      TrailingStop(action:SELL, asset_pair:(ETH, BTC), volume:1.5,
                   offset:0.01, relative:False)
      means: "The maximum is ETH = 0.07 BTC. Keep track of the market and go
              recording the maximum price achieved. If at some point the
              market price goes DOWN by a 0.01BTC respect to the maximum,
              then place the Order(SELL, (ETH, BTC), 1.5)" """

    def __init__(self, action, asset_pair, volume, offset, relative,
                 leverage=None, only_validate=False):
        Order.__init__(self, action, asset_pair, volume, leverage,
                       only_validate)

        if action == 'sell' and offset >= 0:
            raise ValueError('The offset MUST be strictly negative')
        if action == 'buy' and offset <= 0:
            raise ValueError('The offset MUST be strictly positive')
        if not isinstance(relative, bool):
            raise ValueError('The parameter `relative` MUST be a boolean')

        self._offset = offset
        self._relative = relative

    @property
    def offset(self):
        return self._offset

    @property
    def relative(self):
        return self._relative

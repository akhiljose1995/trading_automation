class Portfolio:
    """
    Simulates a trading portfolio.
    Tracks cash, positions, trades, and equity over time.
    """
    def __init__(self, initial_capital=100000):
        """
        :param initial_capital: Starting capital of the portfolio.
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []

    def buy(self, price, timestamp):
        """
        Simulate a buy order.
        :param price: Price at which to buy.
        :param timestamp: Time of the trade.
        """
        qty = self.cash // price
        if qty > 0:
            self.position = qty
            self.cash -= qty * price
            self.trades.append((timestamp, 'BUY', price, qty))

    def sell(self, price, timestamp):
        """
        Simulate a sell order.
        :param price: Price at which to sell.
        :param timestamp: Time of the trade.
        """
        if self.position > 0:
            self.cash += self.position * price
            self.trades.append((timestamp, 'SELL', price, self.position))
            self.position = 0

    def record_equity(self, price):
        """
        Record current portfolio value based on market price.
        :param price: Latest market price.
        """
        equity = self.cash + self.position * price
        self.equity_curve.append(equity)

    def final_value(self, last_price):
        """
        Calculate final portfolio value.
        :param last_price: Last available market price.
        :return: Final capital value.
        """
        return self.cash + self.position * last_price

    def get_equity_curve(self):
        """Return the list of equity values recorded over time."""
        return self.equity_curve

    def get_trades(self):
        """Return the list of trades executed."""
        return self.trades

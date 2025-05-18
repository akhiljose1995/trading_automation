class Backtester:
    """
    Backtesting engine that runs a strategy on historical data
    and simulates trading based on signals.
    """
    def __init__(self, strategy, portfolio):
        """
        :param strategy: Strategy object implementing generate_signals().
        :param portfolio: Portfolio object to track trades and capital.
        """
        self.strategy = strategy
        self.portfolio = portfolio

    def run(self, df):
        """
        Execute the strategy on the given price data.
        :param df: DataFrame with historical price data.
        :return: Portfolio after simulation.
        """
        df = self.strategy.generate_signals(df)

        for i in range(1, len(df)):
            signal = df["signal"].iloc[i]
            price = df["close"].iloc[i]
            timestamp = df.index[i]

            if signal == 1 and self.portfolio.position == 0:
                self.portfolio.buy(price, timestamp)
            elif signal == -1 and self.portfolio.position > 0:
                self.portfolio.sell(price, timestamp)

            self.portfolio.record_equity(price)

        self.portfolio.record_equity(df["close"].iloc[-1])
        return self.portfolio

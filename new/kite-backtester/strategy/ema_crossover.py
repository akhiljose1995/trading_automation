import pandas as pd
from .base import Strategy

class EMACrossoverStrategy(Strategy):
    """
    Implements a simple EMA crossover strategy.
    Buy when short EMA > long EMA, sell when short EMA < long EMA.
    """
    def __init__(self, short_window=9, long_window=20):
        """
        :param short_window: Period for the short EMA.
        :param long_window: Period for the long EMA.
        """
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add EMA and signal columns to the price DataFrame.
        :param df: DataFrame with price data.
        :return: DataFrame with EMA and signal columns.
        """
        df[self.short_window] = df["close"].ewm(span=self.short_window, adjust=False).mean()
        df[self.long_window] = df["close"].ewm(span=self.long_window, adjust=False).mean()
        df["signal"] = 0
        df.loc[df[self.short_window] > df[self.long_window], "signal"] = 1
        df.loc[df[self.short_window] < df[self.long_window], "signal"] = -1
        return df


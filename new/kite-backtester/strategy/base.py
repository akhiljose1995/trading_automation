class Strategy:
    """
    Abstract base class for trading strategies.
    All strategy classes should inherit from this and implement generate_signals().
    """
    def generate_signals(self, df):
        """
        Generate trading signals based on input price DataFrame.
        :param df: pandas DataFrame with market data.
        :return: DataFrame with signal column.
        """
        raise NotImplementedError("Subclasses must implement this method.")

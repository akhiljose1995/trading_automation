import pandas as pd
import numpy as np

class BacktestPortfolio:
    """
    Advanced backtesting portfolio for tracking positions, trades, equity, and performance metrics.
    """

    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0
        self.entry_price = None
        self.equity_curve = []
        self.trades = []

    def buy(self, price, timestamp):
        """
        Executes a buy order using all available cash.
        """
        if self.position == 0:
            qty = self.cash // price
            if qty > 0:
                self.position = qty
                self.entry_price = price
                self.cash -= qty * price
                self.trades.append({
                    'timestamp': timestamp,
                    'type': 'BUY',
                    'price': price,
                    'qty': qty
                })

    def sell(self, price, timestamp):
        """
        Executes a sell order of all held position.
        Calculates and logs PnL.
        """
        if self.position > 0:
            proceeds = self.position * price
            cost = self.position * self.entry_price
            pnl = proceeds - cost
            self.cash += proceeds
            self.trades.append({
                'timestamp': timestamp,
                'type': 'SELL',
                'price': price,
                'qty': self.position,
                'pnl': pnl
            })
            self.position = 0
            self.entry_price = None

    def record_equity(self, price, timestamp):
        """
        Record the total portfolio value at a timestamp.
        """
        total_equity = self.cash + (self.position * price)
        self.equity_curve.append({'timestamp': timestamp, 'equity': total_equity})

    def final_value(self, last_price):
        return self.cash + (self.position * last_price)

    def get_trades(self) -> pd.DataFrame:
        return pd.DataFrame(self.trades)

    def get_equity_curve(self) -> pd.DataFrame:
        return pd.DataFrame(self.equity_curve)

    def performance_metrics(self):
        df = self.get_equity_curve().copy()
        df.set_index("timestamp", inplace=True)
        df["returns"] = df["equity"].pct_change().fillna(0)

        total_return = (df["equity"].iloc[-1] / df["equity"].iloc[0]) - 1
        sharpe = np.mean(df["returns"]) / np.std(df["returns"]) * np.sqrt(252 * 24 * 4)  # Assuming 15-min candles
        drawdown = (df["equity"] / df["equity"].cummax()) - 1
        max_dd = drawdown.min()

        trade_df = self.get_trades()
        wins = trade_df[trade_df['type'] == 'SELL']["pnl"] > 0
        win_rate = wins.mean() if len(wins) > 0 else 0

        return {
            "Total Return (%)": round(total_return * 100, 2),
            "Sharpe Ratio": round(sharpe, 2),
            "Max Drawdown (%)": round(max_dd * 100, 2),
            "Win Rate (%)": round(win_rate * 100, 2),
            "Final Portfolio Value": round(df["equity"].iloc[-1], 2)
        }



import pandas as pd
from .base import BaseReport

class TradeSummary(BaseReport):
    def __init__(self, trades):
        self.trades = trades
        self.report = {}

    def generate(self):
        if not self.trades:
            self.report = {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "avg_profit": 0.0,
                "avg_loss": 0.0,
                "avg_trade_duration": 0,
                "longest_trade_duration": 0,
                "shortest_trade_duration": 0
            }
            return self.report

        df = pd.DataFrame(self.trades, columns=["timestamp", "type", "price", "qty"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        profits = []
        durations = []
        buy_price = buy_time = buy_qty = None

        for _, row in df.iterrows():
            if row["type"] == "BUY":
                buy_price = row["price"]
                buy_qty = row["qty"]
                buy_time = row["timestamp"]
            elif row["type"] == "SELL" and buy_price is not None:
                profit = (row["price"] - buy_price) * buy_qty
                duration = (row["timestamp"] - buy_time).total_seconds() / 60
                profits.append(profit)
                durations.append(duration)
                buy_price = buy_time = buy_qty = None

        profits = pd.Series(profits)
        durations = pd.Series(durations)

        winning = profits[profits > 0]
        losing = profits[profits <= 0]

        self.report = {
            "total_trades": len(profits),
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "win_rate": round(len(winning) / len(profits) * 100, 2) if len(profits) > 0 else 0.0,
            "avg_profit": round(winning.mean(), 2) if not winning.empty else 0.0,
            "avg_loss": round(losing.mean(), 2) if not losing.empty else 0.0,
            "avg_trade_duration": round(durations.mean(), 2) if not durations.empty else 0,
            "longest_trade_duration": round(durations.max(), 2) if not durations.empty else 0,
            "shortest_trade_duration": round(durations.min(), 2) if not durations.empty else 0
        }
        return self.report


import datetime
import matplotlib.pyplot as plt
from strategy import EMACrossoverStrategy
from portfolio.portfolio import Portfolio
from backtester.engine import Backtester
from data.kite_loader import KiteDataLoader
import config
from report.metrics import (
    calculate_roi,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from report.trade_summary import TradeSummary
from report.exporter import export_trades, export_equity_curve
from report.visualizer import EquityCurvePlot


loader = KiteDataLoader(api_key=config.API_KEY, access_token=config.ACCESS_TOKEN, request_token=config.REQUEST_TOKEN, api_secret=config.API_SECRET)
df = loader.get_data(
    instrument_token=config.INSTRUMENT_TOKEN,
    from_date=datetime.datetime(2023, 1, 1),
    to_date=datetime.datetime(2023, 12, 31),
    interval="15minute"
)

strategy = EMACrossoverStrategy()
portfolio = Portfolio(initial_capital=100000)
engine = Backtester(strategy, portfolio)
portfolio = engine.run(df)

# === Getting Equity Curve ===
plot_equity_curve(portfolio.get_equity_curve(), timestamps)

print(f"Final Capital: ₹{portfolio.final_value(df['close'].iloc[-1])}")

# === Performance Metrics ===
roi = calculate_roi(portfolio.get_equity_curve(), portfolio.initial_capital)
max_dd = calculate_max_drawdown(portfolio.get_equity_curve())
sharpe = calculate_sharpe_ratio(portfolio.get_equity_curve())

print("\n--- Performance Summary ---")
print(f"ROI: {roi:.2f}%")
print(f"Max Drawdown: {max_dd:.2f}%")
print(f"Sharpe Ratio: {sharpe:.2f}")

# === Trade Summary ===
#trade_stats = analyze_trades(portfolio.get_trades(), portfolio.initial_capital)
trade_summary = TradeSummary(trades=portfolio.get_trades())
report = trade_summary.generate()

# Export
trade_summary.to_csv("output/trade_summary.csv")
trade_summary.to_json("output/trade_summary.json")

# View
print("\n--- Trade Summary ---")
print(report)

# === Export Reports ===
timestamps = df.index[1:].tolist()
export_trades(portfolio.get_trades())
export_equity_curve(portfolio.get_equity_curve(), timestamps)


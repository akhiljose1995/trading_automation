import pytest
import datetime
from data.kite_loader import KiteDataLoader
from strategy.ema_crossover import EMACrossoverStrategy
from portfolio.backtest_portfolio import BacktestPortfolio
import config


@pytest.fixture(scope="module")
def kite_data():
    """
    Fixture to load historical data using KiteDataLoader
    for a small time range to test the strategy.
    """
    loader = KiteDataLoader(
        api_key=config.API_KEY,
        access_token=config.ACCESS_TOKEN,
        request_token=config.REQUEST_TOKEN,
        api_secret=config.API_SECRET
    )
    df = loader.get_data(
        instrument_token=config.INSTRUMENT_TOKEN,
        from_date=datetime.datetime(2025, 5, 16),
        to_date=datetime.datetime(2025, 5, 17),
        interval="15minute"
    )
    return df


def test_portfolio_with_real_data(kite_data):
    df = kite_data
    assert not df.empty, "Data loading failed — empty DataFrame."

    # Generate signals
    strategy = EMACrossoverStrategy(short_window=5, long_window=20)
    df = strategy.generate_signals(df)

    # Run portfolio simulation
    portfolio = BacktestPortfolio(initial_capital=18147.40)
    for index, row in df.iterrows():
        if row["signal"] == 1:
            portfolio.buy(row["close"], index)
        elif row["signal"] == -1:
            portfolio.sell(row["close"], index)
        portfolio.record_equity(row["close"], index)

    # Assertions and output
    trades = portfolio.get_trades()
    equity = portfolio.get_equity_curve()
    metrics = portfolio.performance_metrics()

    print("\n--- Trades ---")
    print(trades[:])
    print("\n--- Equity Curve ---")
    print(equity[:])
    print("\n--- Performance Metrics ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    assert len(equity) > 0, "Equity curve not recorded."
    assert len(trades) > 0, "No trades executed."




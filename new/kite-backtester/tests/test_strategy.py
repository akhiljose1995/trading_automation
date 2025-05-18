import datetime
import pytest
import pandas as pd
from strategy.ema_crossover import EMACrossoverStrategy
from data.kite_loader import KiteDataLoader
import config

@pytest.fixture(scope="module")
def kite_data():
    """
    Fixture to load historical data using KiteDataLoader
    for a small time range to test the strategy.
    """
    loader = KiteDataLoader(api_key=config.API_KEY, access_token=config.ACCESS_TOKEN, request_token=config.REQUEST_TOKEN, api_secret=config.API_SECRET)
    df = loader.get_data(
        instrument_token=config.INSTRUMENT_TOKEN,
        from_date=datetime.datetime(2025, 5, 16),
        to_date=datetime.datetime(2025, 5, 17),
        interval="15minute"
    )
    return df

def test_ema_crossover_signal_generation(kite_data):
    """
    Test that EMA crossover strategy correctly generates signals.
    Ensures 'signal', 'EMA9', and 'EMA20' columns are created.
    """
    short_window=9
    long_window=20
    strategy = EMACrossoverStrategy(short_window=short_window, long_window=long_window)
    df_signals = strategy.generate_signals(kite_data.copy())

    assert short_window in df_signals.columns, "Missing {short_window} column"
    assert long_window in df_signals.columns, "Missing {long_window} column"
    assert 'signal' in df_signals.columns, "Missing signal column"

    # Check if there are some non-zero signals (at least 1 buy or sell)
    non_zero_signals = df_signals[df_signals['signal'] != 0]
    assert len(non_zero_signals) > 0, "No trading signals generated"

    # Optionally: Check if the crossover logic is valid for a few points
    print(df_signals)
    print(len(df_signals))
    #sample = df_signals.iloc[60]
    sample = df_signals.iloc[int(len(df_signals))-1]
    print(sample)
    if sample[short_window] > sample[long_window]:
        assert sample['signal'] == 1
    elif sample[short_window] < sample[long_window]:
        assert sample['signal'] == -1


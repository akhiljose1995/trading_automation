import pandas as pd
import numpy as np

def calculate_roi(equity_curve, initial_capital):
    """
    Calculate Return on Investment (ROI).
    :param equity_curve: List of equity values over time.
    :param initial_capital: Starting capital.
    :return: ROI in percentage.
    """
    final_value = equity_curve[-1]
    roi = ((final_value - initial_capital) / initial_capital) * 100
    return roi

def calculate_total_return(equity_curve):
    """
    Calculate total return as a decimal (not in %).
    """
    return (equity_curve[-1] / equity_curve[0]) - 1

def calculate_annualized_return(equity_curve, periods_per_year=252 * 26):  # 15min = ~26/day
    """
    Calculate annualized return.
    """
    total_return = calculate_total_return(equity_curve)
    num_periods = len(equity_curve)
    return (1 + total_return) ** (periods_per_year / num_periods) - 1

def calculate_annualized_volatility(equity_curve, periods_per_year=252 * 26):
    """
    Calculate annualized volatility from returns.
    """
    returns = pd.Series(equity_curve).pct_change().dropna()
    return returns.std() * np.sqrt(periods_per_year)

def calculate_sharpe_ratio(equity_curve, risk_free_rate=0.0, periods_per_year=252 * 26):
    """
    Calculate the Sharpe Ratio of the strategy.
    This version is annualized.
    """
    ann_return = calculate_annualized_return(equity_curve, periods_per_year)
    ann_volatility = calculate_annualized_volatility(equity_curve, periods_per_year)
    if ann_volatility == 0:
        return 0.0
    return (ann_return - risk_free_rate) / ann_volatility

def calculate_max_drawdown(equity_curve):
    """
    Calculate the maximum drawdown from the equity curve.
    """
    equity_series = pd.Series(equity_curve)
    rolling_max = equity_series.cummax()
    drawdown = (equity_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100  # in percentage
    return max_drawdown

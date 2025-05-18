import pandas as pd

def export_trades(trades, file_path="output/trades.csv"):
    """
    Export the list of trades to a CSV file.
    
    :param trades: List of (timestamp, type, price, qty)
    :param file_path: Output file path
    """
    df = pd.DataFrame(trades, columns=["timestamp", "type", "price", "qty"])
    df.to_csv(file_path, index=False)
    print(f"Trades exported to {file_path}")

def export_equity_curve(equity_list, timestamps, file_path="output/equity_curve.csv"):
    """
    Export the equity curve values to a CSV file.

    :param equity_list: List of equity values over time.
    :param timestamps: List of corresponding timestamps.
    :param file_path: Output file path
    """
    df = pd.DataFrame({
        "timestamp": timestamps,
        "equity": equity_list
    })
    df.to_csv(file_path, index=False)
    print(f"Equity curve exported to {file_path}")

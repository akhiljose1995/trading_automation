import matplotlib.pyplot as plt
import os

class EquityCurvePlot:
    def __init__(self, equity_curve, timestamps):
        self.equity_curve = equity_curve
        self.timestamps = timestamps
        self.fig = None
        self.ax = None

    def plot(self, show=True):
        """
        Generate the equity curve plot.
        """
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.plot(self.timestamps, self.equity_curve, label="Equity Curve", color='blue')
        self.ax.set_title("Equity Curve")
        self.ax.set_xlabel("Timestamp")
        self.ax.set_ylabel("Equity Value")
        self.ax.grid(True)
        self.ax.legend()
        plt.tight_layout()

        if show:
            plt.show()

    def save(self, path="output/equity_curve.png"):
        """
        Save the plot to file.
        """
        if self.fig is None:
            self.plot(show=False)  # generate silently
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fig.savefig(path)

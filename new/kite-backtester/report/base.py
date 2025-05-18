from abc import ABC, abstractmethod
import pandas as pd
import json
import os

class BaseReport(ABC):
    @abstractmethod
    def generate(self):
        """
        Abstract method to compute the report and populate `self.report`.
        """
        pass

    def to_csv(self, path="report.csv"):
        if hasattr(self, "report"):
            df = pd.DataFrame([self.report])
            df.to_csv(path, index=False)
        else:
            raise ValueError("Report not generated yet. Call `generate()` first.")

    def to_json(self, path="report.json"):
        if hasattr(self, "report"):
            with open(path, "w") as f:
                json.dump(self.report, f, indent=2, default=str)
        else:
            raise ValueError("Report not generated yet. Call `generate()` first.")

    def get_report(self):
        if hasattr(self, "report"):
            return self.report
        else:
            raise ValueError("Report not generated yet. Call `generate()` first.")

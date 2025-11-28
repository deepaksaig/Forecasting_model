"""Simple in-memory store for uploaded datasets."""
from __future__ import annotations

from typing import Dict

import pandas as pd


class DataStore:
    def __init__(self):
        self.sales: Dict[str, pd.DataFrame] = {}

    def save_sales(self, key: str, df: pd.DataFrame):
        self.sales[key] = df

    def get_sales(self, key: str) -> pd.DataFrame:
        return self.sales[key]

    def list_keys(self):
        return list(self.sales.keys())


data_store = DataStore()

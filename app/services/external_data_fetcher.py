"""Mock external data fetchers for regressors."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd


def _generate_time_series(start: datetime, end: datetime, freq: str, column_name: str, seed: int = 42) -> pd.DataFrame:
    rng = pd.date_range(start, end, freq=freq)
    rs = np.random.default_rng(seed)
    values = rs.normal(loc=100, scale=10, size=len(rng))
    return pd.DataFrame({"date": rng, column_name: values})


def fetch_epidemiology(start: datetime, end: datetime, freq: str = "W") -> pd.DataFrame:
    """Mock disease incidence data.

    Represents public health stats such as influenza-like illness rates from UKHSA.
    """
    df = _generate_time_series(start, end, freq, "epi_index", seed=1)
    return df


def fetch_macro(start: datetime, end: datetime, freq: str = "M") -> pd.DataFrame:
    """Mock macroeconomic indicators such as GDP or unemployment."""
    df = _generate_time_series(start, end, freq, "gdp_growth", seed=2)
    df["inflation"] = _generate_time_series(start, end, freq, "inflation", seed=3)["inflation"]
    return df


def fetch_pricing(start: datetime, end: datetime, freq: str = "M") -> pd.DataFrame:
    """Mock pricing and tariff updates representing NHS Drug Tariff data."""
    df = _generate_time_series(start, end, freq, "tariff_price", seed=4)
    return df


def fetch_guideline_events(start: datetime, end: datetime) -> pd.DataFrame:
    """Mock guideline or regulatory events.

    Produces event dummy variables to mimic NICE/MHRA updates.
    """
    rng = pd.date_range(start, end, freq="M")
    df = pd.DataFrame({"date": rng, "guideline_event": 0})
    if len(rng) > 3:
        df.loc[df.index[::4], "guideline_event"] = 1
    return df


def fetch_all_regressors(start: datetime, end: datetime) -> Dict[str, pd.DataFrame]:
    """Return all mock regressors as a dictionary."""
    return {
        "epidemiology": fetch_epidemiology(start, end),
        "macro": fetch_macro(start, end),
        "pricing": fetch_pricing(start, end),
        "guidelines": fetch_guideline_events(start, end),
    }

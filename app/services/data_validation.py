"""Utilities for validating sales data uploads."""
from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

import pandas as pd

REQUIRED_COLUMNS = {"date", "drug_name", "units_sold", "sales_value"}


class ValidationResult:
    def __init__(self, dataframe: pd.DataFrame, issues: List[str], frequency: str):
        self.dataframe = dataframe
        self.issues = issues
        self.frequency = frequency

    def to_message(self) -> str:
        issue_text = "; ".join(self.issues) if self.issues else "No major issues detected"
        return f"Validation complete. {issue_text}."


def _infer_frequency(df: pd.DataFrame) -> str:
    inferred = pd.infer_freq(df["date"].sort_values())
    if inferred:
        return inferred
    # fallback simple heuristic
    deltas = df["date"].sort_values().diff().dropna().value_counts()
    if deltas.empty:
        return "undetermined"
    most_common = deltas.idxmax()
    if most_common.days == 1:
        return "D"
    if most_common.days in {7, 6}:
        return "W"
    if 28 <= most_common.days <= 31:
        return "M"
    return "undetermined"


def validate_sales_csv(file_path: str) -> ValidationResult:
    df = pd.read_csv(file_path)
    issues: List[str] = []

    missing_cols = REQUIRED_COLUMNS.difference(set(df.columns))
    if missing_cols:
        issues.append(f"Missing required columns: {', '.join(sorted(missing_cols))}")

    # Normalize date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        missing_dates = df[df["date"].isna()].shape[0]
        if missing_dates:
            issues.append(f"Found {missing_dates} rows with invalid dates")
        df = df.dropna(subset=["date"])
    else:
        df["date"] = datetime.today()

    frequency = _infer_frequency(df)

    # Fill missing dates for each drug/region combination
    completed_frames = []
    group_cols = ["drug_name"]
    if "region" in df.columns:
        group_cols.append("region")

    for _, group in df.groupby(group_cols):
        date_range = pd.date_range(group["date"].min(), group["date"].max(), freq=frequency if frequency != "undetermined" else "D")
        completed = (
            group.set_index("date").reindex(date_range).rename_axis("date").reset_index()
        )
        completed[group_cols] = completed[group_cols].ffill()
        completed_frames.append(completed)

    completed_df = pd.concat(completed_frames, ignore_index=True)
    completed_df["units_sold"] = completed_df["units_sold"].fillna(0)
    completed_df["sales_value"] = completed_df["sales_value"].fillna(0)

    return ValidationResult(completed_df, issues, frequency)


def summarize_dataframe(df: pd.DataFrame) -> List[str]:
    return [
        f"Rows: {len(df)}",
        f"Date span: {df['date'].min().date()} to {df['date'].max().date()}",
        f"Drugs: {', '.join(df['drug_name'].unique())}",
    ]

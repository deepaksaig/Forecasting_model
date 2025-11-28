import pandas as pd
from datetime import datetime

from app.services.data_validation import validate_sales_csv
from app.services.external_data_fetcher import fetch_all_regressors
from app.services.forecasting import evaluate_models


def test_validate_sales_csv_handles_invalid_and_missing(tmp_path):
    data = """date,drug_name,units_sold,sales_value,region
2022-01-01,DrugA,100,1200,UK
2022-02-01,DrugA,110,1250,UK
2022-XX-01,DrugA,115,1300,UK
2022-04-01,DrugA,130,1400,UK
"""
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(data)

    result = validate_sales_csv(str(csv_path))

    assert any("invalid dates" in issue for issue in result.issues)
    # Should infer monthly frequency and fill the missing March row
    assert result.frequency.startswith("M")
    completed = result.dataframe
    assert len(completed) == 4
    march_row = completed.loc[completed["date"] == pd.Timestamp("2022-03-01")]
    assert not march_row.empty
    assert march_row["units_sold"].iloc[0] == 0


def test_fetch_all_regressors_returns_expected_shapes():
    start = datetime(2022, 1, 1)
    end = datetime(2022, 3, 1)
    regressors = fetch_all_regressors(start, end)

    assert {"epidemiology", "macro", "pricing", "guidelines"}.issubset(regressors.keys())
    for name, df in regressors.items():
        assert not df.empty, f"{name} regressor is empty"
        assert "date" in df.columns


def test_evaluate_models_uses_regressors_when_helpful():
    dates = pd.date_range("2022-01-01", periods=24, freq="M")
    regressor = pd.Series(range(len(dates)), index=dates)
    target = regressor * 1.5 + 10
    df = pd.DataFrame({"date": dates, "units_sold": target, "driver": regressor}).reset_index(drop=True)

    result = evaluate_models(df, target_col="units_sold", horizon=3)

    assert result.name in {"random_forest", "moving_average", "naive", "arima"}
    assert len(result.forecast) == 3
    assert set(result.used_regressors) == {"driver"}

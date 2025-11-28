"""Pydantic schemas for request and response bodies."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class SalesUploadResponse(BaseModel):
    file_id: str
    message: str
    detected_frequency: str
    records: int
    issues: List[str] = []


class DataSourceSuggestion(BaseModel):
    category: str
    description: str
    potential_sources: List[str]
    recommended_frequency: str
    reason_for_relevance: str


class SuggestRequest(BaseModel):
    drug_name: str
    atc_class: Optional[str] = None
    indication: Optional[str] = None
    country: str = "UK"


class SuggestResponse(BaseModel):
    suggestions: List[DataSourceSuggestion]
    search_queries: List[str]


class ForecastRequest(BaseModel):
    drug_name: str
    target_metric: str = Field(..., description="units_sold or sales_value")
    region: Optional[str] = None
    forecast_horizon: int = 12
    regressors: Optional[List[str]] = None
    use_exogenous: bool = True


class ForecastResult(BaseModel):
    model_name: str
    metrics: dict
    forecast: List[float]
    dates: List[date]
    used_regressors: List[str]
    message: Optional[str] = None


class RegressorSummary(BaseModel):
    name: str
    description: str
    coverage_start: date
    coverage_end: date
    missing_ratio: float
    correlation_with_target: Optional[float]


class RegressorResponse(BaseModel):
    regressors: List[RegressorSummary]

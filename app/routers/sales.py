"""Endpoints for uploading and inspecting sales data."""
from __future__ import annotations

import uuid
from fastapi import APIRouter, UploadFile

from app.config import UPLOAD_DIR
from app.models.schemas import RegressorResponse, SalesUploadResponse
from app.services import data_validation, external_data_fetcher, feature_engineering
from app.utils.storage import data_store

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/upload", response_model=SalesUploadResponse)
async def upload_sales(file: UploadFile):
    file_id = uuid.uuid4().hex
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    content = await file.read()
    save_path.write_bytes(content)

    validation = data_validation.validate_sales_csv(str(save_path))
    data_store.save_sales(file_id, validation.dataframe)

    message = validation.to_message()
    return SalesUploadResponse(
        file_id=file_id,
        message=message,
        detected_frequency=validation.frequency,
        records=len(validation.dataframe),
        issues=validation.issues,
    )


@router.get("/regressors/{file_id}", response_model=RegressorResponse)
async def get_regressors(file_id: str, target_metric: str = "units_sold"):
    df = data_store.get_sales(file_id)
    regressors = external_data_fetcher.fetch_all_regressors(df["date"].min(), df["date"].max())
    merged = feature_engineering.align_regressors(df[["date", target_metric]], regressors)
    summaries = feature_engineering.summarize_regressors(merged, target_metric)
    return RegressorResponse(regressors=summaries)

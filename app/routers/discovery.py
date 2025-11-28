"""Endpoints for AI-assisted external data discovery."""
from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import SuggestRequest, SuggestResponse
from app.services import external_data_discovery

router = APIRouter(prefix="/discovery", tags=["discovery"])


@router.post("/suggest", response_model=SuggestResponse)
async def suggest_sources(body: SuggestRequest) -> SuggestResponse:
    suggestions = external_data_discovery.suggest_data_sources(
        drug_name=body.drug_name,
        atc_class=body.atc_class,
        indication=body.indication,
        country=body.country,
    )
    queries = external_data_discovery.generate_search_queries(body.drug_name, body.indication, body.country)
    return SuggestResponse(suggestions=suggestions, search_queries=queries)

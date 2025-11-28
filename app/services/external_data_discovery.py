"""Rule-based external data discovery scaffolding.

This module contains placeholder logic that should later be replaced with LLM-driven
recommendations. Each function includes TODO notes where an API call could be inserted.
"""
from typing import List

from .llm_helper import call_llm


def suggest_data_sources(drug_name: str, atc_class: str | None, indication: str | None, country: str = "UK") -> List[dict]:
    """Return recommended data sources for a given drug.

    TODO: Replace rule-based suggestions with an LLM call via :func:`call_llm`.
    """
    default_sources = [
        {
            "category": "epidemiology",
            "description": "Disease incidence/prevalence for the target indication",
            "potential_sources": ["ONS", "UKHSA", "NHS statistics"],
            "recommended_frequency": "weekly",
            "reason_for_relevance": "Captures demand drivers based on disease burden",
        },
        {
            "category": "pricing",
            "description": "Reference pricing, reimbursement updates, and inflation",
            "potential_sources": ["NHS Drug Tariff", "ONS CPI"],
            "recommended_frequency": "monthly",
            "reason_for_relevance": "Price changes impact sales volumes and value",
        },
        {
            "category": "macro",
            "description": "Macroeconomic indicators",
            "potential_sources": ["ONS GDP", "ONS unemployment"],
            "recommended_frequency": "quarterly",
            "reason_for_relevance": "Consumer spending and budgets may shift over time",
        },
        {
            "category": "guidelines",
            "description": "Clinical guideline updates and regulatory announcements",
            "potential_sources": ["NICE", "MHRA"],
            "recommended_frequency": "event",
            "reason_for_relevance": "Guideline changes alter prescribing patterns",
        },
    ]

    # Example of how an LLM could be integrated later
    _ = call_llm(
        f"Suggest additional data sources for {drug_name} {indication or ''} in {country}."
    )
    return default_sources


def generate_search_queries(drug_name: str, indication: str | None, country: str = "UK") -> List[str]:
    """Generate query strings for external data APIs.

    TODO: Replace templates with dynamic prompts sent to :func:`call_llm`.
    """
    base_queries = [
        f"{indication or drug_name} incidence statistics {country}",
        f"{drug_name} price reimbursement updates {country}",
        f"{drug_name} competitor launch UK",
        f"{indication or drug_name} seasonal patterns NHS {country}",
    ]
    call_llm(f"Generate additional queries for {drug_name} in {country}")
    return base_queries

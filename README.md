# UK Pharma Forecasting Application

This repository contains a FastAPI backend and React frontend that demonstrate an end-to-end workflow for forecasting UK pharmaceutical drug sales using user-provided history and mock external regressors.

## Features
- CSV upload with validation, frequency detection, and gap filling.
- AI-assisted data source suggestions with placeholders for LLM integration.
- Mock connectors for epidemiology, macroeconomic, pricing, and guideline data.
- Feature engineering utilities (lags, rolling windows, calendar variables).
- Simple model selection comparing naive, moving average, ARIMA (if available), and random forest models.
- React UI guiding the user through upload, driver selection, regressor review, modeling, and forecast visualization.

## Project structure
```
app/
  main.py              # FastAPI entry point
  routers/             # API routes (sales, discovery, forecast)
  services/            # Validation, discovery, fetchers, feature engineering, modeling
  models/              # Pydantic schemas
frontend/              # React + Vite UI
requirements.txt       # Python dependencies
```

## Getting started

### Backend
1. Create and activate a virtual environment, then install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
3. Access the interactive docs at `http://localhost:8000/docs`.

### Frontend
1. Install Node.js (>=16) and run:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Open the Vite dev server URL (default `http://localhost:5173`). The UI expects the backend to be reachable at the same host; configure a proxy if needed.

## Usage notes
- A sample dataset is available in `data/sample_sales.csv` for quick testing.
- External data discovery and fetching are mocked; replace TODOs with real API calls and LLM prompts as needed.
- The in-memory datastore is suitable for demo purposes. Swap it for persistent storage for production use.

## Extensibility TODOs
- Integrate actual LLM provider into `app/services/llm_helper.py`.
- Replace mock fetchers in `external_data_fetcher.py` with real connectors (e.g., NHS, ONS APIs).
- Expand model search space and hyperparameter tuning for production-grade forecasts.
- Add authentication and persistent databases for multi-user scenarios.

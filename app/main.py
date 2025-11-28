"""FastAPI application wiring routers and services."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import discovery, forecasting, sales

app = FastAPI(title="UK Pharma Forecasting")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router)
app.include_router(discovery.router)
app.include_router(forecasting.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the UK pharma forecasting API"}

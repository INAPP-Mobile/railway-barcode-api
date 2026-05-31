"""Pydantic schemas for the Barcode API."""

from pydantic import BaseModel
from typing import Optional


class BarcodeResponse(BaseModel):
    """Response model for barcode endpoints (when returning JSON instead of raw bytes)."""
    format: str
    data: str
    content_type: str
    barcode: str  # base64-encoded image data


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str

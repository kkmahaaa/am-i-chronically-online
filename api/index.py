"""
FastAPI serverless function for Vercel.
Handles screen time data entry and analytics endpoints.

Why FastAPI: Built-in async support, automatic OpenAPI docs, Pydantic validation,
and excellent performance. Perfect for serverless functions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date
import sys
import os

# Import processing module from same directory
from .processing import analyze_entries

# Initialize FastAPI app
# Why: FastAPI automatically generates OpenAPI docs and handles request/response validation
app = FastAPI(
    title="Am I Chronically Online API",
    description="API for analyzing screen time habits",
    version="1.0.0"
)

# CORS middleware - allows frontend to call API
# Why: Next.js frontend will be on a different origin, so we need CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (simple dict keyed by user_id)
# Why: Easy to replace with database later. Structure is simple: {user_id: [entries]}
# For MVP, we'll use a default "default_user" but this can be extended with auth
_storage = {"default_user": []}


# Pydantic Models for Request/Response Validation
# Why: Automatic validation, type safety, and clear API contracts

class ScreenTimeEntry(BaseModel):
    """Model for a single screen time entry."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    app: str = Field(..., min_length=1, description="App name")
    time_minutes: float = Field(..., gt=0, description="Time spent in minutes")
    category: Optional[str] = Field(None, description="App category (optional, auto-categorized if not provided)")
    pickups: Optional[int] = Field(None, ge=0, description="Number of times app was opened")
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        """Validate date format."""
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


class EntriesRequest(BaseModel):
    """Request model for submitting multiple entries."""
    entries: List[ScreenTimeEntry] = Field(..., min_length=1, description="List of screen time entries")
    user_id: Optional[str] = Field("default_user", description="User identifier (for multi-user support)")


class AnalyticsResponse(BaseModel):
    """Response model for analytics endpoint."""
    success: bool
    metrics: dict
    chronic_score: dict
    tips: List[dict]
    processed_entries_count: int


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Am I Chronically Online API",
        "status": "running",
        "endpoints": {
            "POST /api/entries": "Submit screen time entries",
            "GET /api/analytics": "Get analytics for stored entries"
        }
    }


@app.post("/api/entries")
async def submit_entries(request: EntriesRequest):
    """
    Submit daily screen time entries.
    
    Why: POST endpoint allows frontend to send data. We validate with Pydantic,
    store entries, and immediately return analytics for instant feedback.
    """
    try:
        user_id = request.user_id or "default_user"
        
        # Convert Pydantic models to dicts for processing
        entries_dict = [entry.model_dump() for entry in request.entries]
        
        # Store entries (append to existing)
        if user_id not in _storage:
            _storage[user_id] = []
        _storage[user_id].extend(entries_dict)
        
        # Process and return analytics immediately
        result = analyze_entries(_storage[user_id])
        
        return {
            "success": True,
            "message": f"Successfully added {len(request.entries)} entries",
            "total_entries": len(_storage[user_id]),
            "analytics": {
                "metrics": result["metrics"],
                "chronic_score": result["chronic_score"],
                "tips": result["tips"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing entries: {str(e)}")


@app.get("/api/analytics")
async def get_analytics(user_id: str = "default_user"):
    """
    Get analytics for all stored entries.
    
    Why: GET endpoint allows frontend to fetch analytics without resubmitting data.
    Useful for dashboard refreshes or viewing historical data.
    """
    try:
        if user_id not in _storage or len(_storage[user_id]) == 0:
            return {
                "success": True,
                "message": "No entries found",
                "metrics": {},
                "chronic_score": {
                    "score": 0,
                    "level": "Unknown",
                    "description": "No data available"
                },
                "tips": [],
                "processed_entries_count": 0
            }
        
        # Process all stored entries
        result = analyze_entries(_storage[user_id])
        
        return {
            "success": True,
            "metrics": result["metrics"],
            "chronic_score": result["chronic_score"],
            "tips": result["tips"],
            "processed_entries_count": result["processed_entries_count"],
            "total_entries": len(_storage[user_id])
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating analytics: {str(e)}")


@app.delete("/api/entries")
async def clear_entries(user_id: str = "default_user"):
    """
    Clear all entries for a user (useful for testing/resetting).
    
    Why: DELETE endpoint allows users to start fresh. In production, you might
    want to add authentication/authorization checks.
    """
    if user_id in _storage:
        _storage[user_id] = []
    
    return {
        "success": True,
        "message": f"Cleared all entries for user: {user_id}"
    }


# Vercel serverless function handler
# Why: Vercel expects a handler function that takes (event, context)
# Mangum adapter converts ASGI (FastAPI) to AWS Lambda format that Vercel uses
def handler(event, context):
    """Vercel serverless function handler."""
    try:
        from mangum import Mangum
        asgi_handler = Mangum(app)
        return asgi_handler(event, context)
    except ImportError:
        # Fallback for local development
        # In production, Vercel will handle this automatically
        return {
            "statusCode": 200,
            "body": "FastAPI app initialized. Use uvicorn for local development."
        }

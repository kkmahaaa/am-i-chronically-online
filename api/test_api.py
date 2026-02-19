"""
Test script for Phase 2 API endpoints.
Run with: python api/test_api.py

Make sure the API server is running first:
    uvicorn api.index:app --reload --port 8000
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_submit_entries():
    """Test POST /api/entries endpoint."""
    print("=" * 60)
    print("Testing POST /api/entries")
    print("=" * 60)
    
    test_entries = [
        {
            "date": "2024-01-20",
            "app": "Instagram",
            "time_minutes": 120,
            "pickups": 15
        },
        {
            "date": "2024-01-20",
            "app": "TikTok",
            "time_minutes": 90,
            "pickups": 20
        },
        {
            "date": "2024-01-20",
            "app": "Gmail",
            "time_minutes": 30,
            "pickups": 5
        },
        {
            "date": "2024-01-21",
            "app": "Instagram",
            "time_minutes": 150,
            "pickups": 18
        },
        {
            "date": "2024-01-21",
            "app": "YouTube",
            "time_minutes": 180,
            "pickups": 10
        }
    ]
    
    payload = {
        "entries": test_entries,
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/entries", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Added {len(test_entries)} entries")
        print(f"Total entries stored: {data['total_entries']}")
        print(f"\nChronic Score: {data['analytics']['chronic_score']['score']}/100")
        print(f"Level: {data['analytics']['chronic_score']['level']}")
        print(f"\nTop Tips:")
        for i, tip in enumerate(data['analytics']['tips'][:3], 1):
            print(f"  {i}. {tip['title']}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False


def test_get_analytics():
    """Test GET /api/analytics endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/analytics")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/analytics", params={"user_id": "test_user"})
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success!")
        print(f"Total Screen Time: {data['metrics']['total_screen_time_hours']} hours")
        print(f"Doomscroll Hours: {data['metrics']['doomscroll_hours']} hours")
        print(f"Days Tracked: {data['metrics']['days_tracked']}")
        print(f"Chronic Score: {data['chronic_score']['score']}/100 - {data['chronic_score']['level']}")
        print(f"Tips Available: {len(data['tips'])}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False


def test_root():
    """Test root endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        data = response.json()
        print(f"✅ API Status: {data['status']}")
        print(f"Message: {data['message']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n🧪 Testing Phase 2: API Endpoints")
    print("Make sure the server is running: uvicorn api.index:app --reload --port 8000\n")
    
    # Test root endpoint first
    if not test_root():
        print("\n⚠️  Could not connect to API. Is the server running?")
        print("Start it with: uvicorn api.index:app --reload --port 8000")
        exit(1)
    
    # Test endpoints
    test_submit_entries()
    test_get_analytics()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

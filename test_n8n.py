#!/usr/bin/env python3
"""
Test script for n8n integration endpoint
"""

import requests
import json

# Test data matching your n8n webhook format
test_data = [
    {
        "keywords": [
            "IPTV restream business models US entrepreneurs",
            "Monetization strategies IPTV streaming US",
            "IPTV service revenue generation US",
            "Launching IPTV restream platform US",
            "Subscription video on demand business US"
        ],
        "geo": "US",
        "method": "combined",
        "startTime": "2025-08-01T00:00:00.000Z",
        "endTime": "2025-08-31T00:00:00.000Z",
        "userId": "030874c9-55aa-4d20-8ece-5140fba0b798"
    }
]

def test_n8n_endpoint():
    """Test the n8n endpoint with sample data"""
    
    # Test the debug endpoint first
    print("🔍 Testing n8n debug endpoint...")
    try:
        response = requests.post(
            "http://localhost:8001/n8n/test",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test the actual n8n endpoint
    print("🚀 Testing n8n keyword check endpoint...")
    try:
        response = requests.post(
            "http://localhost:8001/n8n/check-keywords",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Country: {result['country']}")
            print(f"Method: {result['method']}")
            print(f"Total Keywords: {result['total_keywords']}")
            print(f"Keywords: {result['keywords']}")
            print(f"Results: {json.dumps(result['results'], indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_n8n_endpoint()

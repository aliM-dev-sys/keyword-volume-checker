#!/usr/bin/env python3
"""
Simple test script to verify the Keyword Volume Checker API is working correctly.
Run this after starting the API server to test all endpoints.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_KEYWORDS = ["seo", "marketing", "digital marketing", "content strategy"]
TEST_COUNTRY = "US"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_single_keyword():
    """Test single keyword volume check"""
    print("\n🔍 Testing single keyword check...")
    try:
        response = requests.get(
            f"{BASE_URL}/check-volume",
            params={"keyword": "seo", "country": TEST_COUNTRY}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Single keyword check passed: {data['keyword']} = {data['volume']:,} volume")
            return True
        else:
            print(f"❌ Single keyword check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Single keyword check failed: {e}")
        return False

def test_batch_keywords():
    """Test batch keyword volume check"""
    print("\n🔍 Testing batch keyword check...")
    try:
        response = requests.post(
            f"{BASE_URL}/check-batch",
            json={"keywords": TEST_KEYWORDS, "country": TEST_COUNTRY}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Batch keyword check passed: {len(data['results'])} keywords processed")
            for result in data['results']:
                print(f"   - {result['keyword']}: {result['volume']:,} volume")
            return True
        else:
            print(f"❌ Batch keyword check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Batch keyword check failed: {e}")
        return False

def test_export_csv():
    """Test CSV export functionality"""
    print("\n🔍 Testing CSV export...")
    try:
        keywords_str = ",".join(TEST_KEYWORDS)
        response = requests.get(
            f"{BASE_URL}/export/csv",
            params={"keywords": keywords_str, "country": TEST_COUNTRY}
        )
        if response.status_code == 200:
            print("✅ CSV export passed")
            return True
        else:
            print(f"❌ CSV export failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
        return False

def test_export_json():
    """Test JSON export functionality"""
    print("\n🔍 Testing JSON export...")
    try:
        keywords_str = ",".join(TEST_KEYWORDS)
        response = requests.get(
            f"{BASE_URL}/export/json",
            params={"keywords": keywords_str, "country": TEST_COUNTRY}
        )
        if response.status_code == 200:
            print("✅ JSON export passed")
            return True
        else:
            print(f"❌ JSON export failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ JSON export failed: {e}")
        return False

def test_web_dashboard():
    """Test web dashboard accessibility"""
    print("\n🔍 Testing web dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and "Keyword Volume Checker" in response.text:
            print("✅ Web dashboard accessible")
            return True
        else:
            print(f"❌ Web dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web dashboard failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Keyword Volume Checker API Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_single_keyword,
        test_batch_keywords,
        test_export_csv,
        test_export_json,
        test_web_dashboard
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
        print(f"\n🌐 Access the web dashboard at: {BASE_URL}")
        print(f"📚 API documentation at: {BASE_URL}/docs")
    else:
        print("⚠️  Some tests failed. Check the API server logs for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

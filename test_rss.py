#!/usr/bin/env python3
"""
Simple test to verify RSS feed accessibility
"""

import requests

def test_rss_feed():
    """Test if RSS feed is accessible"""
    try:
        url = "https://blog.shrivarshapoojary.in/index.xml"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ RSS feed is accessible!")
            # Show first 500 characters
            content_preview = response.text[:500]
            print("\nContent Preview:")
            print(content_preview)
        else:
            print("❌ RSS feed returned error status")
            
    except Exception as e:
        print(f"❌ Error accessing RSS feed: {e}")

if __name__ == "__main__":
    test_rss_feed()

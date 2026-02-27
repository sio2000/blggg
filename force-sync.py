#!/usr/bin/env python3
"""
Force sync all articles to Netlify
This script will sync your local articles to Netlify automatically
"""

import requests
import json
import sys

def sync_to_netlify(base_url):
    """Sync articles to the given URL"""
    try:
        print(f"Syncing articles to: {base_url}")
        
        # Call the sync API
        response = requests.post(f"{base_url}/api/sync-articles", timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS: {result['message']}")
            print(f"  Local articles: {result['localCount']}")
            print(f"  Netlify articles: {result['netlifyCount']}")
            return True
        else:
            print(f"✗ FAILED: HTTP {response.status_code}")
            print(f"  Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to {base_url}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_sync_status(base_url):
    """Check sync status"""
    try:
        response = requests.get(f"{base_url}/api/sync-articles", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result['netlifyCount']} Netlify, {result['localCount']} Local")
            print(f"In sync: {'YES' if result['inSync'] else 'NO'}")
            return result
        else:
            print(f"Failed to check status: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error checking status: {e}")
        return None

def main():
    print("=== FORCE SYNC ARTICLES TO NETLIFY ===\n")
    
    # Try different URLs in order
    urls_to_try = [
        "http://localhost:3000",           # Local development
        "https://your-blog-name.netlify.app",  # Replace with your actual URL
    ]
    
    # Try to detect if we're running on Netlify
    if "netlify" in sys.executable.lower() or "netlify" in os.getcwd().lower():
        print("Detected Netlify environment")
        urls_to_try.insert(0, "https://your-blog-name.netlify.app")  # Put Netlify first
    
    success = False
    
    for url in urls_to_try:
        print(f"\nTrying: {url}")
        
        # Check status first
        status = check_sync_status(url)
        
        # Try to sync
        if sync_to_netlify(url):
            success = True
            break
        
        print("Trying next URL...\n")
    
    if success:
        print("\n🎉 SYNC COMPLETE!")
        print("All articles should now be available on your site.")
        print("Wait 1-2 minutes for changes to propagate.")
    else:
        print("\n❌ SYNC FAILED!")
        print("Please check:")
        print("1. Your site is running")
        print("2. Update the URL in this script to match your Netlify site")
        print("3. Run this script again")

if __name__ == '__main__':
    import os
    main()

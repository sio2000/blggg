#!/usr/bin/env python3
"""
Script to sync local articles to Netlify Blobs
This will upload all articles from .data/articles.json to Netlify production
"""

import json
import requests
import os
from datetime import datetime

def load_local_articles():
    """Load articles from local .data/articles.json file"""
    try:
        with open('.data/articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"✓ Loaded {len(articles)} articles from .data/articles.json")
        return articles
    except FileNotFoundError:
        print("✗ .data/articles.json not found")
        return []
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing .data/articles.json: {e}")
        return []

def upload_to_netlify(article):
    """Upload a single article to Netlify via API"""
    try:
        # Your Netlify site URL - replace with your actual Netlify URL
        netlify_url = "https://your-blog-name.netlify.app"  # UPDATE THIS
        
        # For testing, you can use localhost first
        # netlify_url = "http://localhost:3000"
        
        api_url = f"{netlify_url}/api/articles"
        
        payload = {
            'title': article['title'],
            'content': article['content'],
            'imageUrl': article.get('imageUrl'),
            'author': article.get('author', 'Katerina Mistrioti'),
            'labels': article.get('labels', []),
            'category': article.get('category', 'Αρχική σελίδα')
        }
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 201:
            print(f"  ✓ Uploaded: {article['title'][:50]}...")
            return True
        else:
            print(f"  ✗ Failed to upload: {article['title'][:50]}... - {response.status_code}")
            print(f"    Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error uploading {article['title'][:50]}...: {e}")
        return False

def main():
    print("=== Syncing Local Articles to Netlify ===\n")
    
    # Load local articles
    articles = load_local_articles()
    if not articles:
        print("No articles to sync. Exiting.")
        return
    
    print(f"\nStarting upload of {len(articles)} articles...\n")
    
    # Upload each article
    success_count = 0
    failed_count = 0
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Processing: {article['title'][:50]}...")
        
        if upload_to_netlify(article):
            success_count += 1
        else:
            failed_count += 1
        
        # Small delay to avoid overwhelming the server
        import time
        time.sleep(0.5)
    
    print(f"\n=== Sync Complete ===")
    print(f"✓ Successfully uploaded: {success_count} articles")
    print(f"✗ Failed to upload: {failed_count} articles")
    
    if failed_count == 0:
        print("\n🎉 All articles have been successfully synced to Netlify!")
        print("Please check your Netlify site to verify all articles are visible.")
    else:
        print(f"\n⚠️  {failed_count} articles failed to upload. Please check the errors above.")

if __name__ == '__main__':
    main()

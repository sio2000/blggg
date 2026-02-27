#!/usr/bin/env python3
"""
Upload all articles to Netlify
Replace YOUR_NETLIFY_URL with your actual Netlify site URL
"""

import json
import requests
import time

def load_articles():
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def upload_all_articles():
    articles = load_articles()
    print(f"Loaded {len(articles)} articles from .data/articles.json")
    
    # REPLACE THIS WITH YOUR ACTUAL NETLIFY URL
    netlify_url = "https://your-blog-name.netlify.app"  # <-- UPDATE THIS
    
    # For testing, you can start with localhost
    # netlify_url = "http://localhost:3000"
    
    print(f"Target URL: {netlify_url}")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] {article['title'][:60]}...")
        
        try:
            response = requests.post(
                f"{netlify_url}/api/articles",
                json={
                    'title': article['title'],
                    'content': article['content'],
                    'imageUrl': article.get('imageUrl'),
                    'author': article.get('author', 'Katerina Mistrioti'),
                    'labels': article.get('labels', []),
                    'category': article.get('category', 'Αρχική σελίδα')
                },
                timeout=30
            )
            
            if response.status_code == 201:
                print(f"  ✓ Success")
                success += 1
            else:
                print(f"  ✗ Failed: HTTP {response.status_code}")
                if response.text:
                    error_text = response.text[:100]
                    print(f"    Error: {error_text}...")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Connection failed - check URL and network")
            failed += 1
            break
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
        
        # Rate limiting
        time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print("UPLOAD COMPLETE")
    print("=" * 60)
    print(f"✓ Successfully uploaded: {success} articles")
    print(f"✗ Failed to upload: {failed} articles")
    
    if success > 0:
        print(f"\n🎉 {success} articles are now on your Netlify site!")
        print("Visit your site to verify all articles are visible.")

if __name__ == '__main__':
    # Check if URL needs to be updated
    with open('upload-all-articles.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'your-blog-name.netlify.app' in content:
            print("⚠️  PLEASE UPDATE THE NETLIFY URL IN THIS SCRIPT FIRST!")
            print("Open upload-all-articles.py and replace 'your-blog-name.netlify.app' with your actual Netlify site URL")
            print("\nThen run this script again.")
        else:
            upload_all_articles()

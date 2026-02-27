#!/usr/bin/env python3
"""
Simple test script to upload articles to localhost
"""

import json
import requests
import time

def load_articles():
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def upload_to_localhost():
    articles = load_articles()
    print(f"Loaded {len(articles)} articles")
    
    success = 0
    failed = 0
    
    for i, article in enumerate(articles[:5]):  # Test with first 5 articles
        print(f"[{i+1}/5] Uploading: {article['title'][:50]}...")
        
        try:
            response = requests.post(
                "http://localhost:3000/api/articles",
                json={
                    'title': article['title'],
                    'content': article['content'],
                    'imageUrl': article.get('imageUrl'),
                    'author': article.get('author', 'Katerina Mistrioti'),
                    'labels': article.get('labels', []),
                    'category': article.get('category', 'Αρχική σελίδα')
                },
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"  ✓ Success")
                success += 1
            else:
                print(f"  ✗ Failed: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
        
        time.sleep(0.5)
    
    print(f"\nResult: {success} success, {failed} failed")

if __name__ == '__main__':
    upload_to_localhost()

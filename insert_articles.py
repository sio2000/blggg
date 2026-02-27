#!/usr/bin/env python3
"""
Script to insert scraped articles into the database via API
"""

import requests
import json

def insert_article(article):
    """Insert a single article via API"""
    try:
        response = requests.post('http://localhost:3000/api/articles', json={
            'title': article['title'],
            'content': article['content'],
            'imageUrl': article['imageUrl'],
            'author': article['author'],
            'labels': article['labels'],
            'category': article['category']
        })
        
        if response.status_code == 201:
            print(f"✓ Inserted: {article['title']}")
            return True
        else:
            print(f"✗ Failed to insert: {article['title']} - {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error inserting {article['title']}: {e}")
        return False

def main():
    # Load scraped articles
    with open('scraped_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Inserting {len(articles)} articles...")
    
    success_count = 0
    for article in articles:
        if insert_article(article):
            success_count += 1
    
    print(f"\nSuccessfully inserted {success_count}/{len(articles)} articles")

if __name__ == '__main__':
    main()

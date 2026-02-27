#!/usr/bin/env python3
"""
Script to directly insert scraped articles into the local JSON database
"""

import json
import os
from datetime import datetime
import shutil

def main():
    # Load scraped articles
    with open('scraped_articles.json', 'r', encoding='utf-8') as f:
        scraped_articles = json.load(f)
    
    # Ensure .data directory exists
    data_dir = '.data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Load existing articles if they exist
    articles_file = os.path.join(data_dir, 'articles.json')
    existing_articles = []
    
    if os.path.exists(articles_file):
        with open(articles_file, 'r', encoding='utf-8') as f:
            existing_articles = json.load(f)
    
    print(f"Found {len(existing_articles)} existing articles")
    print(f"Adding {len(scraped_articles)} new articles")
    
    # Convert scraped articles to the correct format
    new_articles = []
    for article in scraped_articles:
        # Convert to the expected Article format
        formatted_article = {
            "id": article["id"],
            "title": article["title"],
            "content": article["content"],
            "imageUrl": article["imageUrl"],
            "published": article["published"],
            "author": article["author"],
            "labels": article["labels"],
            "category": article["category"],
            "createdAt": datetime.now().isoformat()
        }
        new_articles.append(formatted_article)
    
    # Combine articles - new ones first
    all_articles = new_articles + existing_articles
    
    # Save back to file
    with open(articles_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(all_articles)} total articles to {articles_file}")
    
    # Show article titles
    print("\nAdded articles:")
    for article in new_articles:
        print(f"  - {article['title']}")

if __name__ == '__main__':
    main()

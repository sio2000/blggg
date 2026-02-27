#!/usr/bin/env python3
"""
Script to move new articles from the beginning to the middle of the list
"""

import json
import os

def main():
    # Load current articles
    articles_file = '.data/articles.json'
    
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Total articles: {len(articles)}")
    
    # The new articles are the first 11 (diet-web articles)
    new_articles = articles[:11]
    existing_articles = articles[11:]
    
    # Calculate middle position
    middle_index = len(existing_articles) // 2
    
    # Create new order: existing first half + new articles + existing second half
    first_half = existing_articles[:middle_index]
    second_half = existing_articles[middle_index:]
    
    reordered_articles = first_half + new_articles + second_half
    
    print(f"Moved {len(new_articles)} articles to position {middle_index}")
    
    # Save reordered articles
    with open(articles_file, 'w', encoding='utf-8') as f:
        json.dump(reordered_articles, f, ensure_ascii=False, indent=2)
    
    print("Articles reordered successfully!")
    
    # Show new positions of moved articles
    print("\nNew positions of moved articles:")
    for i, article in enumerate(new_articles):
        position = middle_index + i + 1  # +1 for 1-based indexing
        print(f"  {position}. {article['title']}")

if __name__ == '__main__':
    main()

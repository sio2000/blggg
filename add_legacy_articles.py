#!/usr/bin/env python3
"""
Script to add legacy articles from content.json and then move new articles to middle
"""

import json
import os

def main():
    # Load scraped articles
    with open('scraped_articles.json', 'r', encoding='utf-8') as f:
        new_articles = json.load(f)
    
    # Load legacy articles from content.json
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
    
    legacy_articles = content_data.get('posts', [])
    
    print(f"Found {len(legacy_articles)} legacy articles")
    print(f"Found {len(new_articles)} new articles")
    
    # Convert legacy articles to the correct format
    formatted_legacy = []
    for article in legacy_articles:
        formatted_article = {
            "id": article["id"],
            "title": article["title"],
            "content": article["content"],
            "imageUrl": None,  # Legacy articles don't have imageUrl
            "published": article["published"],
            "author": article["author"],
            "labels": article.get("labels", []),
            "category": "Αρχική σελίδα",
            "createdAt": article["published"]  # Use published as createdAt
        }
        formatted_legacy.append(formatted_article)
    
    # Convert new articles to correct format
    formatted_new = []
    for article in new_articles:
        formatted_article = {
            "id": article["id"],
            "title": article["title"],
            "content": article["content"],
            "imageUrl": article["imageUrl"],
            "published": article["published"],
            "author": article["author"],
            "labels": article["labels"],
            "category": article["category"],
            "createdAt": "2025-02-27T06:20:00.000Z"  # Current time
        }
        formatted_new.append(formatted_article)
    
    # Calculate middle position
    middle_index = len(formatted_legacy) // 2
    
    # Create final order: legacy first half + new articles + legacy second half
    first_half = formatted_legacy[:middle_index]
    second_half = formatted_legacy[middle_index:]
    
    final_articles = first_half + formatted_new + second_half
    
    # Ensure .data directory exists
    if not os.path.exists('.data'):
        os.makedirs('.data')
    
    # Save to articles.json
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(final_articles, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully created articles list with {len(final_articles)} total articles")
    print(f"New articles placed at position {middle_index + 1}")
    
    print("\nNew article positions:")
    for i, article in enumerate(formatted_new):
        position = middle_index + i + 1
        print(f"  {position}. {article['title']}")

if __name__ == '__main__':
    main()

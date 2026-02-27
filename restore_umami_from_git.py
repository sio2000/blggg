#!/usr/bin/env python3
"""
Restore the Umami article content from the git-restored legacy file
"""

import json

def main():
    print("=== RESTORING UMAMI FROM GIT ===\n")
    
    # Get the original content from legacy file
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
    
    # Find the Umami article in legacy
    target_title = "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!"
    original_content = None
    
    for article in legacy_articles:
        if article.get('title', '').strip() == target_title:
            original_content = article.get('content', '')
            break
    
    if not original_content:
        print("Original Umami content not found!")
        return
    
    print(f"Found original content with length: {len(original_content)}")
    
    # Load current articles
    db_articles = []
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
    
    # Update the database version
    for article in db_articles:
        if article.get('title', '').strip() == target_title:
            print(f"Restoring database version")
            article['content'] = original_content
            break
    
    # Save database articles
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(db_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(db_articles)} articles to .data/articles.json")
    
    # The legacy version is already correct from git restore
    print("Legacy version is already correct from git restore")
    
    print("\n=== RESTORATION COMPLETE ===")
    print("The Umami article has been restored to its original content!")
    print("Now we can make the precise deletions as requested in οδηγίες.txt")

if __name__ == '__main__':
    main()

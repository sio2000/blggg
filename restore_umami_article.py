#!/usr/bin/env python3
"""
Restore the Umami article from backup or from the other source
"""

import json

def main():
    print("=== RESTORING UMAMI ARTICLE ===\n")
    
    # Load current articles
    current_articles = []
    
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
        for article in db_articles:
            article['source_file'] = '.data/articles.json'
            current_articles.append(article)
    
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
        for article in legacy_articles:
            article['source_file'] = 'src/lib/content.json'
            current_articles.append(article)
    
    # Try to find the original Umami article from any backup or other source
    target_title = "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!"
    
    # Check if we have any other copies or if we can restore from git
    print("Looking for original Umami article content...")
    
    # First, let's check if there's a backup in scraped_articles.json
    try:
        with open('scraped_articles.json', 'r', encoding='utf-8') as f:
            scraped_articles = json.load(f)
            
        for scraped_article in scraped_articles:
            scraped_title = scraped_article.get('title', '').strip()
            if "Umami" in scraped_title and "βάρος" in scraped_title:
                print(f"Found original in scraped_articles.json: {scraped_title}")
                print(f"Content length: {len(scraped_article.get('content', ''))}")
                
                # Restore this content to both current articles
                for current_article in current_articles:
                    if current_article.get('title', '').strip() == target_title:
                        print(f"Restoring content to {current_article['source_file']}")
                        current_article['content'] = scraped_article.get('content', '')
                
                break
        else:
            print("Original not found in scraped_articles.json")
            
    except FileNotFoundError:
        print("scraped_articles.json not found")
    
    # If we can't find the original, let's at least restore from the other source
    # Check if the two versions have different content
    db_version = None
    legacy_version = None
    
    for article in current_articles:
        if article.get('title', '').strip() == target_title:
            if article.get('source_file') == '.data/articles.json':
                db_version = article
            elif article.get('source_file') == 'src/lib/content.json':
                legacy_version = article
    
    if db_version and legacy_version:
        db_content = db_version.get('content', '')
        legacy_content = legacy_version.get('content', '')
        
        print(f"Database version content length: {len(db_content)}")
        print(f"Legacy version content length: {len(legacy_content)}")
        
        # If one is significantly longer, restore from that one
        if len(db_content) > len(legacy_content) * 1.5:
            print("Restoring legacy version from database version")
            legacy_version['content'] = db_content
        elif len(legacy_content) > len(db_content) * 1.5:
            print("Restoring database version from legacy version")
            db_version['content'] = legacy_content
        else:
            print("Both versions seem similar, cannot restore original content")
    
    # Save the restored articles
    db_articles = []
    legacy_articles = []
    
    for article in current_articles:
        if article.get('source_file') == '.data/articles.json':
            db_articles.append(article)
        elif article.get('source_file') == 'src/lib/content.json':
            legacy_article = {
                'id': article.get('id'),
                'published': article.get('published'),
                'updated': article.get('updated'),
                'title': article.get('title'),
                'content': article.get('content'),
                'labels': article.get('labels', []),
                'link': article.get('link', ''),
                'author': article.get('author')
            }
            legacy_articles.append(legacy_article)
    
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(db_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(db_articles)} articles to .data/articles.json")
    
    content_data = {
        'posts': legacy_articles
    }
    with open('src/lib/content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(legacy_articles)} articles to src/lib/content.json")
    
    print("\n=== RESTORATION COMPLETE ===")
    print("Please check if the Umami article content has been restored properly.")

if __name__ == '__main__':
    main()

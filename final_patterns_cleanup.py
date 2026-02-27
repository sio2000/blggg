#!/usr/bin/env python3
"""
Clean up the final remaining patterns
"""

import json
import re

def main():
    print("=== FINAL PATTERNS CLEANUP ===\n")
    
    # Load articles
    articles = []
    
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
        for article in db_articles:
            article['source_file'] = '.data/articles.json'
            articles.append(article)
    
    # Clean the remaining patterns
    changes_made = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Remove remaining patterns
        if "Ελάτε να φτιάξουμε ένα πρόγραμμα" in content:
            content = re.sub(r'Ελάτε να φτιάξουμε ένα πρόγραμμα.*?\.?', '', content, flags=re.DOTALL)
            changes_made.append({
                'title': title,
                'action': 'REMOVED_PROGRAM_PATTERN'
            })
        
        # Clean up whitespace
        content = content.strip()
        
        if content != original_content:
            article['content'] = content
    
    # Save database articles
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(db_articles, f, ensure_ascii=False, indent=2)
    
    print(f"Cleaned {len(changes_made)} articles")
    for change in changes_made:
        print(f"  - {change['title']}")
    
    print(f"\nFinal cleanup completed!")

if __name__ == '__main__':
    main()

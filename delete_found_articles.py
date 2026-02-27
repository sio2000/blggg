#!/usr/bin/env python3
"""
Script to delete the found articles completely
"""

import json

def main():
    print("=== DELETING FOUND ARTICLES ===\n")
    
    # Load articles
    articles = []
    
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
        for article in db_articles:
            article['source_file'] = '.data/articles.json'
            articles.append(article)
    
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
        for article in legacy_articles:
            article['source_file'] = 'src/lib/content.json'
            articles.append(article)
    
    # Articles to delete (with exact titles found)
    delete_titles = [
        "Τα άτομα με υψηλότερη μόρφωση  (ή ανώτερο πνευματικό επίπεδο) είναι ενήμερα για την Εναλλακτική Ιατρική"
    ]
    
    # Also search for articles with "Προβιοτικά" and "στήθος"
    probiotic_articles = []
    
    changes_made = []
    
    # Filter out articles to delete
    filtered_db_articles = []
    filtered_legacy_articles = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        
        # Check for exact title match
        should_delete = False
        for delete_title in delete_titles:
            if title == delete_title:
                should_delete = True
                break
        
        # Check for probiotic + chest articles
        if "Προβιοτικά" in title and "στήθος" in title:
            should_delete = True
        
        if should_delete:
            changes_made.append({
                'title': title,
                'id': article.get('id'),
                'source_file': article.get('source_file'),
                'action': 'DELETED_COMPLETELY'
            })
            print(f"DELETED: {title} from {article.get('source_file')}")
        else:
            # Keep the article
            if article.get('source_file') == '.data/articles.json':
                filtered_db_articles.append(article)
            elif article.get('source_file') == 'src/lib/content.json':
                # Remove extra fields for legacy format
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
                filtered_legacy_articles.append(legacy_article)
    
    # Save filtered articles
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_db_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(filtered_db_articles)} articles to .data/articles.json")
    
    content_data = {
        'posts': filtered_legacy_articles
    }
    with open('src/lib/content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(filtered_legacy_articles)} articles to src/lib/content.json")
    
    # Report
    print(f"\nComplete deletions: {len(changes_made)}")
    for change in changes_made:
        print(f"  - {change['title']} ({change['source_file']})")
    
    # Save report
    report = {
        'complete_deletions': changes_made,
        'total_deletions': len(changes_made),
        'timestamp': '2025-02-27T06:40:00Z'
    }
    
    with open('final_deletion_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal deletion report saved to final_deletion_report.json")

if __name__ == '__main__':
    main()

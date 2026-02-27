#!/usr/bin/env python3
"""
Aggressive cleanup of Umami article
"""

import json
import re

def main():
    print("=== AGGRESSIVE UMAMI CLEANUP ===\n")
    
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
    
    changes_made = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this is the Umami article
        if "Umami" in title and "βάρος" in title:
            print(f"Processing: {title}")
            
            # Aggressive patterns to delete everything related to the proposal
            aggressive_patterns = [
                # Delete everything from "Πρόταση:" to the end of that section
                r'Πρόταση:.*?(?=<br|$|</div>)',
                
                # Delete any remaining fragments
                r'Τακτικός.*?ανά.*?τρίμηνο.*?',
                r'ολοκλήρου.*?οργανισμού.*?με.*?«.*?».*?από.*?την.*?',
                r'Η.*?του.*?«.*?».*?προσφέρει.*?δυνατότητα.*?',
                r'μέθοδος.*?είναι.*?εξαιρετικά.*?οικονομική.*?',
                r'60.*?90.*?λεπτά.*?ώρας.*?',
                r'Περισσότερες.*?πληροφορίες.*?μέθοδο.*?βρείτε.*?',
                r'που.*?αναφέρεται.*?αποκλειστικά.*?στο.*?«.*?».*?',
                
                # Clean up empty tags and broken references
                r'<b>\s*«\s*»\s*</b>',
                r'«\s*»\s*\.?',
                r'&nbsp;\s*«\s*»\s*&nbsp;',
                r'\s*«\s*»\s*',
                
                # Clean up any remaining proposal-related content
                r'Πρόταση.*',
                r'Τεχνολογία.*?Βιοσυντονισμού.*',
                r'Sensitiv.*?Imago.*',
                r'Κατερίνα.*?Μηστριώτη.*',
                r'\*.*',
            ]
            
            for pattern in aggressive_patterns:
                new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'AGGRESSIVE_CLEANUP',
                        'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                    })
                    content = new_content
                    print(f"  ✅ Applied aggressive cleanup")
            
            # Clean up multiple spaces and line breaks
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'<br/>\s*<br/>\s*<br/>', '<br/><br/>', content)
            content = content.strip()
            
            if content != original_content:
                article['content'] = content
                print(f"  ✅ Updated {title}")
    
    # Save articles
    db_articles = []
    legacy_articles = []
    
    for article in articles:
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
    
    # Report
    print(f"\n=== AGGRESSIVE CLEANUP REPORT ===")
    print(f"Total aggressive cleanups: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['pattern']}")
    
    # Save report
    report = {
        'aggressive_cleanups': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T07:30:00Z'
    }
    
    with open('aggressive_umami_cleanup_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nAggressive cleanup report saved to aggressive_umami_cleanup_report.json")

if __name__ == '__main__':
    main()

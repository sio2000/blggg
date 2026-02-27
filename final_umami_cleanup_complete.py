#!/usr/bin/env python3
"""
Final cleanup of remaining Umami fragments
"""

import json
import re

def main():
    print("=== FINAL UMAMI CLEANUP ===\n")
    
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
            
            # Delete all remaining fragments
            final_patterns = [
                # Delete the entire proposal section
                r'&nbsp;\s*Τακτικός\s*–\s*ανά\s*τρίμηno\s*-\s*έλεγχος\s*κατάστασης\s*της\s*υγείας-διατροφικών\s*ελλείψεων\s*και\s*μεταβολισμού\s*-\s*ολοκλήρου\s*του\s*οργανισμού\s*με\s*&nbsp;<b>\s*«\s*»\s*</b>\s*από\s*την\s*Κατερίνα\s*Μηστριώτη\s*\*',
                
                # Delete any remaining proposal fragments
                r'Τακτικός.*?ανά.*?τρίμηνο.*?έλεγχος.*?κατάστασης.*?υγείας.*?διατροφικών.*?ελλείψεων.*?μεταβολισμού.*?ολοκλήρου.*?οργανισμού.*?με.*?',
                
                # Delete empty references
                r'που\s*αναφέρεται\s*αποκλειστικά\s*στο\s*&nbsp;<b>\s*&nbsp;\s*</b>',
                r'«\s*»\s*από\s*την\s*Κατερίνα\s*Μηστριώτη\s*\*',
                r'<b>\s*«\s*»\s*</b>',
                r'«\s*»\s*\.',
                
                # Clean up any remaining asterisks or broken elements
                r'\s*\*\s*$',
                r'^\s*\*\s*',
                r'<b>\s*&nbsp;\s*</b>'
            ]
            
            for pattern in final_patterns:
                new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'FINAL_CLEANUP',
                        'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                    })
                    content = new_content
                    print(f"  ✅ Final cleanup applied")
            
            # Clean up whitespace and formatting
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
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
    print(f"\n=== FINAL UMAMI CLEANUP REPORT ===")
    print(f"Total final cleanups: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['pattern']}")
    
    # Save report
    report = {
        'final_umami_cleanups': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T07:45:00Z'
    }
    
    with open('final_umami_cleanup_complete_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal Umami cleanup report saved to final_umami_cleanup_complete_report.json")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Clean up remaining forbidden phrases from the 5 articles
"""

import json
import re

def main():
    print("=== CLEANUP REMAINING FORBIDDEN PHRASES ===\n")
    
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
    
    # Articles with issues from the verification
    problematic_articles = [
        "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!",
        "Φυσικά Αφροδισιακά για άνδρες και γυναίκες", 
        "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!",
        "Κάνοντας Δίαιτα…. παχαίνετε !!!!"
    ]
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this is one of the problematic articles
        if title in problematic_articles:
            print(f"Processing: {title}")
            
            # Clean up remaining forbidden patterns
            cleanup_patterns = [
                # Author name variations
                r'Κατερίνα\s*Μηστριώτη',
                r'Κατερίνα\s*Μυστριώτη',
                
                # Technology references
                r'Τεχνολογία\s*Βιοσυντονισμού',
                r'Sensitiv\s*Imago',
                
                # Time references
                r'60\s*–\s*90\s*λεπτά\s*της\s*ώρας',
                
                # Any remaining proposal fragments
                r'Πρόταση:.*',
                r'Τακτικός.*?ανά.*?τρίμηνο.*',
                r'ολοκλήρου.*?οργανισμού.*?με.*',
                
                # Clean up broken HTML and extra spaces
                r'<b>\s*&nbsp;\s*</b>',
                r'&nbsp;\s*;\s*&nbsp;',
                r'\s*&nbsp;\s*',
                r'<span[^>]*>\s*&nbsp;\s*</span>',
                
                # Any remaining asterisks or broken elements
                r'^\s*\*\s*$',
                r'\s*\*\s*$',
                r'<br/>\s*<br/>\s*<br/>',
                r'\n\s*\n\s*\n'
            ]
            
            for pattern in cleanup_patterns:
                new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'FORBIDDEN_CLEANUP',
                        'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                    })
                    content = new_content
                    print(f"  ✅ Cleaned pattern")
            
            # Final cleanup
            content = re.sub(r'\s+', ' ', content)
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
    print(f"\n=== CLEANUP REMAINING FORBIDDEN REPORT ===")
    print(f"Total cleanups: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['title']} ({change['source_file']}) - {change['pattern']}")
    
    # Save report
    report = {
        'cleanup_remaining_forbidden': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T07:50:00Z'
    }
    
    with open('cleanup_remaining_forbidden_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nCleanup remaining forbidden report saved to cleanup_remaining_forbidden_report.json")

if __name__ == '__main__':
    main()

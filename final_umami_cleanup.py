#!/usr/bin/env python3
"""
Final cleanup of remaining Umami article text
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
    
    # Specific patterns to delete from Umami article
    umami_patterns = [
        # The main proposal text
        r'Πρόταση:\s*Τακτικός\s*–\s*ανά\s*τρίμηνο\s*–\s*έλεγχος\s*κατάστασης\s*της\s*υγείας-διατροφικών\s*ελλείψεων\s*και\s*μεταβολισμού\s*–\s*ολόκληρου\s*του\s*οργανισμού\s*με\s*«[^»]*»\s*από\s*την\s*\*',
        
        # The capability description
        r'Η\s*του\s*«[^»]*»\s*προσφέρει\s*τη\s*δυνατότητα\s*να\s*έχουμε\s*πλήρη\s*εικόνα\s*της\s*υγείας,\s*των\s*διατροφικών\s*μας\s*ελλείψεων\s*και\s*της\s*κατάστασης\s*του\s*μεταβολισμού\s*μας\s*και\s*εντοπίζει\s*διαταραχές\s*στο\s*αρχικό\s*στάδιο\s*ακόμη\s*και\s*πριν\s*εκδηλωθούν\.',
        
        # The method description
        r'Η\s*μέθοδος\s*είναι\s*εξαιρετικά\s*οικονομική,\s*μη\s*επεμβατική,\s*ανώδυνη,\s*ακίνδυνη\s*ακόμη\s*και\s*σε\s*παιδιά\s*και\s*ο\s*χρόνος\s*που\s*απαιτείται\s*είναι\s*μόνον\s*60\s*–\s*90\s*λεπτά\s*της\s*ώρας\.',
        
        # Any remaining fragments
        r'60\s*–\s*90\s*λεπτά\s*της\s*ώρας',
        r'Περισσότερες\s*πληροφορίες\s*για\s*τη\s*μέθοδο\s*θα\s*βρείτε\s*στο\s*τμήμα\s*της\s*σελίδας\s*του\s*blog\s*που\s*αναφέρεται\s*αποκλειστικά\s*στο\s*«[^»]*»\s*\.?',
    ]
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this is the Umami article
        if "Umami" in title and "βάρος" in title:
            print(f"Processing: {title}")
            
            # Apply all Umami patterns
            for pattern in umami_patterns:
                new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'UMAMI_PATTERN_REMOVED',
                        'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                    })
                    content = new_content
            
            # Clean up whitespace
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
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
    print(f"\n=== UMAMI CLEANUP REPORT ===")
    print(f"Total Umami cleanups: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['pattern']}")
    
    # Save report
    report = {
        'umami_cleanups': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T07:00:00Z'
    }
    
    with open('umami_cleanup_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nUmami cleanup report saved to umami_cleanup_report.json")

if __name__ == '__main__':
    main()

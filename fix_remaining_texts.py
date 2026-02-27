#!/usr/bin/env python3
"""
Fix the remaining texts that were not properly deleted
"""

import json
import re

def load_articles():
    """Load articles from both sources"""
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
    
    return articles

def fix_remaining_texts(articles):
    """Fix the remaining texts that were not properly deleted"""
    
    changes_made = []
    
    # Define the exact remaining patterns to delete
    remaining_patterns = {
        "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!": [
            # The broken text that remains
            r'Πρόταση:\s*Τακτικός\s*–\s*ανά\s*τρίμηνο\s*-\s*έλεγχος\s*κατάστασης\s*της\s*υγείας-διατροφικών\s*ελλείψεων\s*και\s*μεταβολισμού\s*-\s*ολοκλήρου\s*του\s*οργανισμού\s*με\s*«[^»]*»\s*από\s*την\s*\.',
            
            # Any remaining fragments
            r'Τακτικός\s*–\s*ανά\s*τρίμηνο\s*-\s*έλεγχος\s*κατάστασης\s*της\s*υγείας-διατροφικών\s*ελλείψεων\s*και\s*μεταβολισμού\s*-\s*ολοκλήρου\s*του\s*οργανισμού\s*με\s*«[^»]*»\s*από\s*την\s*\*',
            
            r'Η\s*του\s*«[^»]*»\s*προσφέρει\s*τη\s*δυνατότητα\s*να\s*έχουμε\s*πλήρη\s*εικόνα\s*της\s*υγείας',
            r'Η\s*μέθοδος\s*είναι\s*εξαιρετικά\s*οικονομική',
            r'60\s*–\s*90\s*λεπτά\s*της\s*ώρας',
            r'Περισσότερες\s*πληροφορίες\s*για\s*τη\s*μέθοδο\s*θα\s*βρείτε\s*στο\s*τμήμα\s*της\s*σελίδας\s*του\s*blog\s*που\s*αναφέρεται\s*αποκλειστικά\s*στο\s*«[^»]*»',
            
            # Clean up any remaining broken references
            r'που\s*αναφέρεται\s*αποκλειστικά\s*στο\s*«[^»]*»',
            r'«[^»]*»\s*\.',
            r'«[^»]*»\s*&nbsp;'
        ]
    }
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this article has remaining patterns
        if title in remaining_patterns:
            print(f"Processing: {title}")
            
            for pattern in remaining_patterns[title]:
                # Apply the pattern
                new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                if new_content != content:
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'REMAINING_TEXT_DELETED',
                        'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                    })
                    content = new_content
                    print(f"  ✅ Deleted remaining text")
            
            # Clean up whitespace
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip()
            
            if content != original_content:
                article['content'] = content
    
    return articles, changes_made

def save_articles(articles):
    """Save articles back to their respective files"""
    
    # Separate by source file
    db_articles = []
    legacy_articles = []
    
    for article in articles:
        if article.get('source_file') == '.data/articles.json':
            db_articles.append(article)
        elif article.get('source_file') == 'src/lib/content.json':
            # Remove the extra fields for legacy format
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
    
    # Save database articles
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(db_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(db_articles)} articles to .data/articles.json")
    
    # Save legacy articles
    content_data = {
        'posts': legacy_articles
    }
    with open('src/lib/content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(legacy_articles)} articles to src/lib/content.json")

def main():
    print("=== FIXING REMAINING TEXTS ===\n")
    
    # Load articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Fix remaining texts
    modified_articles, changes_made = fix_remaining_texts(articles)
    
    # Save changes
    save_articles(modified_articles)
    
    # Report
    print(f"\n=== REMAINING TEXTS FIX REPORT ===")
    print(f"Total fixes applied: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['title']} ({change['source_file']}) - {change['action']}")
    
    # Save report
    report = {
        'remaining_texts_fixes': changes_made,
        'total_fixes': len(changes_made),
        'timestamp': '2025-02-27T07:25:00Z'
    }
    
    with open('remaining_texts_fix_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nRemaining texts fix report saved to remaining_texts_fix_report.json")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Final cleanup of remaining patterns
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

def apply_final_cleanup(articles):
    """Apply final cleanup to remove all remaining patterns"""
    
    changes_made = []
    
    # Define comprehensive cleanup patterns
    cleanup_patterns = [
        # Contact information
        (r'6975\s*301223', ''),
        (r'mistrioti@gmail\.com', ''),
        (r'k\.mistrioti@yahoo\.gr', ''),
        
        # Call to action phrases
        (r'Ελάτε να φτιάξουμε.*?προγράμ[αα]', ''),
        (r'Επικοινωνήστε μαζί μου.*?\.?', ''),
        (r'Μιλήστε μαζί μας.*?χρειάζεste!!!', ''),
        
        # Sensitiv Imago related
        (r'Sensitiv\s*Imago', ''),
        (r'Τεχνολογία Βιοσυντονισμού.*?\.?', ''),
        (r'Τεχνολογία Βιοσυντονισμού', ''),
        (r'έλεγχος.*?Sensitiv.*?\.?', ''),
        
        # Terra papers
        (r'terra\s*papers', ''),
        (r'άρθρο που δημοσιεύτηκε στο.*?\.?', ''),
        
        # Tags and labels
        (r'Ετικέτες\s*.*? Coaching', ''),
        (r'Ετικέτες\s*.*? Nutrition', ''),
        
        # Author signatures
        (r'Κατερίνα Μηστριώτη.*?διατροφολόγος.*?\.?', ''),
        (r'Κατερίνα Μηστριώτη.*?\.?', ''),
        
        # Website references
        (r'edw hellas', ''),
        (r'www\..*?\.com', ''),
        (r'http://.*?\.com', ''),
        
        # Miscellaneous cleanup
        (r'\*\*\*\*', ''),
        (r'—+', ''),
        (r'\s+', ' '),  # Multiple spaces to single space
        (r'\n\s*\n\s*\n', '\n\n'),  # Multiple newlines to double newline
    ]
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Apply all cleanup patterns
        for pattern, replacement in cleanup_patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
            if new_content != content:
                changes_made.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'action': 'PATTERN_CLEANED',
                    'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                })
                content = new_content
        
        # Clean up whitespace
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
    print("=== FINAL CLEANUP ===\n")
    
    # Load articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Apply cleanup
    cleaned_articles, changes_made = apply_final_cleanup(articles)
    
    # Save changes
    save_articles(cleaned_articles)
    
    # Report
    print(f"\n=== CLEANUP REPORT ===")
    print(f"Total cleanups applied: {len(changes_made)}")
    
    # Group by article
    by_article = {}
    for change in changes_made:
        title = change['title']
        if title not in by_article:
            by_article[title] = []
        by_article[title].append(change)
    
    for title, changes in by_article.items():
        print(f"\n{title}: {len(changes)} cleanups")
        for change in changes:
            print(f"  - {change['pattern']}")
    
    # Save report
    report = {
        'cleanup_changes': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T06:50:00Z'
    }
    
    with open('final_cleanup_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal cleanup report saved to final_cleanup_report.json")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Thorough cleanup of any remaining text fragments
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

def thorough_cleanup(articles):
    """Apply thorough cleanup to remove any remaining fragments"""
    
    changes_made = []
    
    # Specific cleanup patterns for remaining fragments
    cleanup_patterns = [
        # Phone number fragments
        (r'6975\s*301223', ''),
        (r'6975\s*301223', ''),
        (r'\(10πμ\.-19μμ\.\)', ''),
        (r'10πμ-19μμ', ''),
        
        # Email fragments  
        (r'mistrioti@gmail\.com', ''),
        (r'k\.mistrioti@yahoo\.gr', ''),
        
        # Website fragments
        (r'terra\s*papers', ''),
        (r'edw\s*hellas', ''),
        (r'www\..*?\.com', ''),
        (r'http://.*?\.com', ''),
        
        # Tag fragments
        (r'Ετικέτες\s*.*? Coaching', ''),
        (r'Ετικέτες\s*.*? Nutrition', ''),
        
        # Author signature fragments
        (r'Κατερίνα Μηστριώτη.*?διατροφολόγος', ''),
        (r'Κατερίνα Μηστριώτη.*?\.?', ''),
        (r'κλινική διατροφολόγος', ''),
        (r'Κλινική Διατροφόλογος', ''),
        (r'Σύμβουλος Ολιστικών Εφαρμογών', ''),
        (r'σύμβουλος κλινικής διατροφολογίας', ''),
        
        # Article reference fragments
        (r'άρθρο που δημοσιεύτηκε στο.*?\.?', ''),
        (r'δημοσιεύτηκε στο.*?\.?', ''),
        
        # Call to action fragments
        (r'Επικοινώνησε μαζί μου.*?\.?', ''),
        (r'Ελάτε να φτιάξουμε.*?\.?', ''),
        (r'απλά επικοινωνήστε μαζί μου.*?\.?', ''),
        (r'επικοινωνήστε μαζί μου.*?\.?', ''),
        
        # Method fragments
        (r'μέθοδος.*?Sensitiv.*?\.?', ''),
        (r'Τεχνολογία Βιοσυντονισμού.*?\.?', ''),
        (r'Sensitiv\s*Imago', ''),
        
        # General cleanup
        (r'\*\*\*', ''),
        (r'—+', ''),
        (r'\s+', ' '),  # Multiple spaces to single space
        (r'\n\s*\n\s*\n', '\n\n'),  # Multiple newlines to double newline
        (r'\s*<br/>\s*<br/>\s*', '<br/><br/>'),  # Clean up break tags
        (r'\s*</div>\s*<div', '</div><div'),  # Clean up div spacing
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
                    'action': 'FRAGMENT_CLEANED',
                    'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern
                })
                content = new_content
        
        # Clean up whitespace at the end
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
    print("=== THOROUGH CLEANUP OF REMAINING FRAGMENTS ===\n")
    
    # Load articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Apply thorough cleanup
    cleaned_articles, changes_made = thorough_cleanup(articles)
    
    # Save changes
    save_articles(cleaned_articles)
    
    # Report
    print(f"\n=== THOROUGH CLEANUP REPORT ===")
    print(f"Total fragment cleanups applied: {len(changes_made)}")
    
    # Group by article
    by_article = {}
    for change in changes_made:
        title = change['title']
        if title not in by_article:
            by_article[title] = []
        by_article[title].append(change)
    
    for title, changes in by_article.items():
        print(f"\n{title}: {len(changes)} fragment cleanups")
        for change in changes:
            print(f"  - {change['pattern']}")
    
    # Save report
    report = {
        'fragment_cleanups': changes_made,
        'total_cleanups': len(changes_made),
        'timestamp': '2025-02-27T06:55:00Z'
    }
    
    with open('thorough_cleanup_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nThorough cleanup report saved to thorough_cleanup_report.json")

if __name__ == '__main__':
    main()

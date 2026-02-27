#!/usr/bin/env python3
"""
Make precise deletions from Umami article according to οδηγίες.txt
"""

import json
import re

def main():
    print("=== PRECISE UMAMI DELETIONS ===\n")
    
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
    
    # The exact text to delete from οδηγίες.txt line 23-27
    umami_deletion_text = """     Πρόταση:\xa0 Τακτικός – ανά τρίμηνο - έλεγχος κατάστασης της υγείας-διατροφικών ελλείψεων και μεταβολισμού - ολοκλήρου του οργανισμού με\xa0Τεχνολογία Βιοσυντονισμού «Sensitiv Imago»\xa0από την Κατερίνα Μηστριώτη *
*   Η Τεχνολογία Βιοσυντονισμού του\xa0 «Sensitiv Imago»\xa0\xa0προσφέρει την δυνατότητα\xa0να έχουμε πλήρη εικόνα της υγείας, των διατροφικών μας ελλείψεων και της κατάστασης του μεταβολισμού μας και εντοπίζει διαταραχές στο αρχικό στάδιο ακόμη και πριν εκδηλωθούν. \xa0
\xa0   \xa0 Η μέθοδος είναι εξαιρετικά οικονομική, μη επεμβατική, ανώδυνη, ακίνδυνη ακόμη και σε παιδιά και ο χρόνος που απαιτείται είναι μόνον 60 – 90 λεπτά της ώρας.

   Περισσότερες πληροφορίες για την μέθοδο θα βρείτε στο τμήμα της σελίδας του\xa0blog\xa0που αναφέρεται αποκλειστικά στο\xa0«Sensitiv Imago».\xa0"""
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this is the Umami article
        if "Umami" in title and "βάρος" in title:
            print(f"Processing: {title}")
            
            # Try exact match first
            if umami_deletion_text in content:
                content = content.replace(umami_deletion_text, '')
                changes_made.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'action': 'EXACT_DELETION',
                    'deleted_length': len(umami_deletion_text)
                })
                print(f"  ✅ Deleted exact text ({len(umami_deletion_text)} characters)")
            else:
                print(f"  ❌ Exact text not found, trying pattern matching...")
                
                # Try to find and delete with pattern matching for variations
                # Handle non-breaking spaces and other variations
                normalized_deletion = umami_deletion_text.replace('\xa0', ' ').replace('\u200b', '').strip()
                normalized_content = content.replace('\xa0', ' ').replace('\u200b', ' ')
                
                if normalized_deletion in normalized_content:
                    # Use regex for flexible matching
                    pattern = re.escape(normalized_deletion)
                    pattern = pattern.replace(r'\s+', r'\s*')  # Allow for whitespace variations
                    pattern = pattern.replace(r'\*', r'\*')  # Escape asterisks properly
                    
                    new_content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                    if new_content != content:
                        content = new_content
                        changes_made.append({
                            'title': title,
                            'id': article.get('id'),
                            'source_file': article.get('source_file'),
                            'action': 'PATTERN_DELETION'
                        })
                        print(f"  ✅ Deleted with pattern matching")
                else:
                    # Try individual line deletions
                    lines_to_delete = [
                        "Πρόταση:  Τακτικός – ανά τρίμηνο - έλεγχος κατάστασης της υγείας-διατροφικών ελλείψεων και μεταβολισμού - ολοκλήρου του οργανισμού με  Τεχνολογία Βιοσυντονισμού «Sensitiv Imago»  από την Κατερίνα Μηστριώτη *",
                        "Η Τεχνολογία Βιοσυντονισμού του  «Sensitiv Imago»  προσφέρει την δυνατότητα να έχουμε πλήρη εικόνα της υγείας, των διατροφικών μας ελλείψεων και της κατάστασης του μεταβολισμού μας και εντοπίζει διαταραχές στο αρχικό στάδιο ακόμη και πριν εκδηλωθούν. ",
                        "Η μέθοδος είναι εξαιρετικά οικονομική, μη επεμβατική, ανώδυνη, ακίνδυνη ακόμη και σε παιδιά και ο χρόνος που απαιτείται είναι μόνον 60 – 90 λεπτά της ώρας.",
                        "Περισσότερες πληροφορίες για την μέθοδο θα βρείτε στο τμήμα της σελίδας του blog που αναφέρεται αποκλειστικά στο «Sensitiv Imago»."
                    ]
                    
                    for line in lines_to_delete:
                        if line in content:
                            content = content.replace(line, '')
                            changes_made.append({
                                'title': title,
                                'id': article.get('id'),
                                'source_file': article.get('source_file'),
                                'action': 'LINE_DELETION',
                                'deleted_line': line[:50] + '...' if len(line) > 50 else line
                            })
                            print(f"  ✅ Deleted line: {line[:50]}...")
            
            # Clean up extra whitespace
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
    print(f"\n=== PRECISE UMAMI DELETION REPORT ===")
    print(f"Total deletions: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['title']} ({change['source_file']}) - {change['action']}")
    
    # Save report
    report = {
        'precise_umami_deletions': changes_made,
        'total_deletions': len(changes_made),
        'timestamp': '2025-02-27T07:35:00Z'
    }
    
    with open('precise_umami_deletions_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nPrecise Umami deletions report saved to precise_umami_deletions_report.json")

if __name__ == '__main__':
    main()

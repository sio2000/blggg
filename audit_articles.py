#!/usr/bin/env python3
"""
Script to audit articles and find the 17 specific articles + 2 additional ones
"""

import json
import os

def load_articles():
    """Load articles from both sources"""
    articles = []
    
    # Load from .data/articles.json (database)
    try:
        with open('.data/articles.json', 'r', encoding='utf-8') as f:
            db_articles = json.load(f)
            for article in db_articles:
                article['source'] = 'database'
                articles.append(article)
        print(f"Loaded {len(db_articles)} articles from database")
    except Exception as e:
        print(f"Error loading database articles: {e}")
    
    # Load from src/lib/content.json (legacy)
    try:
        with open('src/lib/content.json', 'r', encoding='utf-8') as f:
            content_data = json.load(f)
            legacy_articles = content_data.get('posts', [])
            for article in legacy_articles:
                article['source'] = 'legacy'
                articles.append(article)
        print(f"Loaded {len(legacy_articles)} articles from legacy")
    except Exception as e:
        print(f"Error loading legacy articles: {e}")
    
    return articles

def find_target_articles(articles):
    """Find the 17 specific articles + 2 additional ones"""
    
    # Target articles to find
    target_titles = [
        "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα! Ξεκινάμε ΣΗΜΕΡΑ",
        "Φυσικά Αφροδισιακά για άνδρες και γυναίκες",
        "Umami και…χάνουμε βάρος, τρώγοντας περισσότερο !!!",
        "Κάνοντας Δίαιτα…. παχαίνετε !!!!",
        "Φρούτα, τα οφέλη και οι αντιθέσεις τους",
        "Βιολογικά Προϊόντα Μύθοι και Αλήθειες",
        "4 μικρά μυστικά και χάνετε 2-4 κιλά",
        "Τροφές που μπλοκάρουν την απώλεια κιλών",
        "Αδυνατείστε με υδατάνθρακες",
        "Η σεροτονίνη φέρνει ευτυχία κι επιτυχία",
        "Μαγγάνιο το πολύτιμο μέταλλο",
        "Το σωσίβιο είναι επικίνδυνο",
        "Το πάχος ξεκινά και ρυθμίζεται από τον εγκέφαλο",
        "Η Διατροφή κατα της γρίπης",
        "Λεπτίνη, η ορμόνη ρυθμιστής της Ενέργειας",
        "Παραμείνετε λεπτοί χωρίς δίαιτα"
    ]
    
    # Additional articles to delete completely
    delete_titles = [
        "Τα άτομα με υψηλότερη μόρφωση (ή ανώτερο πνευματικό επίπεδο) είναι ενήμερα για την Εναλλακτική Ιατρική",
        "Προβιοτικά …και για το στήθος !!!!"
    ]
    
    found_articles = []
    duplicates = {}
    
    for article in articles:
        title = article.get('title', '').strip()
        
        # Check if it's one of the target articles
        for target_title in target_titles:
            if title == target_title:
                found_articles.append({
                    'title': title,
                    'id': article.get('id'),
                    'source': article.get('source'),
                    'content_preview': article.get('content', '')[:200] + '...' if len(article.get('content', '')) > 200 else article.get('content', '')
                })
                
                # Track duplicates
                if title not in duplicates:
                    duplicates[title] = []
                duplicates[title].append({
                    'id': article.get('id'),
                    'source': article.get('source')
                })
                break
        
        # Check if it's one of the articles to delete completely
        for delete_title in delete_titles:
            if title == delete_title:
                found_articles.append({
                    'title': title,
                    'id': article.get('id'),
                    'source': article.get('source'),
                    'delete_completely': True,
                    'content_preview': article.get('content', '')[:200] + '...' if len(article.get('content', '')) > 200 else article.get('content', '')
                })
                
                if title not in duplicates:
                    duplicates[title] = []
                duplicates[title].append({
                    'id': article.get('id'),
                    'source': article.get('source')
                })
                break
    
    return found_articles, duplicates

def main():
    print("=== AUDIT OF ARTICLES ===\n")
    
    # Load all articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Find target articles
    found_articles, duplicates = find_target_articles(articles)
    
    print("=== FOUND TARGET ARTICLES ===")
    for article in found_articles:
        print(f"\nTitle: {article['title']}")
        print(f"ID: {article['id']}")
        print(f"Source: {article['source']}")
        if article.get('delete_completely'):
            print("ACTION: DELETE COMPLETELY")
        else:
            print("ACTION: DELETE SPECIFIC TEXT")
        print(f"Content preview: {article['content_preview']}")
    
    print("\n=== DUPLICATES ANALYSIS ===")
    for title, entries in duplicates.items():
        if len(entries) > 1:
            print(f"\nDUPLICATE FOUND: {title}")
            for entry in entries:
                print(f"  - ID: {entry['id']}, Source: {entry['source']}")
        else:
            print(f"\nUNIQUE: {title}")
    
    # Save audit results
    audit_result = {
        'found_articles': found_articles,
        'duplicates': duplicates,
        'total_articles_checked': len(articles)
    }
    
    with open('audit_results.json', 'w', encoding='utf-8') as f:
        json.dump(audit_result, f, ensure_ascii=False, indent=2)
    
    print(f"\nAudit results saved to audit_results.json")
    print(f"Found {len(found_articles)} target articles out of {len(articles)} total")

if __name__ == '__main__':
    main()

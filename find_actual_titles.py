#!/usr/bin/env python3
"""
Find the actual titles of articles that should match the target articles
"""

import json

def main():
    print("=== FINDING ACTUAL TITLES ===\n")
    
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
    
    # Target keywords from οδηγίες.txt
    target_keywords = [
        ("Κάθε μέρα", "νέο σώμα"),
        ("Φυσικά Αφροδισιακά", "άνδρες και γυναίκες"),
        ("Umami", "βάρος"),
        ("Κάνοντας Δίαιτα", "παχαίνετε"),
        ("Φρούτα", "αντιθέσεις"),
        ("Βιολογικά Προϊόντα", "Μύθοι"),
        ("4 μικρά μυστικά", "2-4 κιλά"),
        ("Τροφές", "απώλεια κιλών"),
        ("Αδυνατείστε", "υδατάνθρακες"),
        ("σεροτονίνη", "ευτυχία"),
        ("Μαγγάνιο", "μέταλλο"),
        ("σωσίβιο", "επικίνδυνο"),
        ("πάχος", "εγκέφαλος"),
        ("Διατροφή", "γρίπης"),
        ("Λεπτίνη", "Ενέργειας"),
        ("Παραμείνετε", "δίαιτα")
    ]
    
    found_articles = []
    
    for article in articles:
        title = article.get('title', '').strip()
        
        for keywords in target_keywords:
            if all(keyword.lower() in title.lower() for keyword in keywords):
                found_articles.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'keywords': keywords
                })
                break
    
    print(f"Found {len(found_articles)} articles matching target keywords:")
    
    for i, article in enumerate(found_articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Keywords: {article['keywords']}")
        print(f"   Source: {article['source_file']}")
        print(f"   ID: {article['id']}")
    
    # Check for duplicates
    print(f"\n=== DUPLICATE CHECK ===")
    titles_count = {}
    for article in found_articles:
        title = article['title']
        if title not in titles_count:
            titles_count[title] = []
        titles_count[title].append(article)
    
    for title, entries in titles_count.items():
        if len(entries) > 1:
            print(f"DUPLICATE: {title} ({len(entries)} copies)")
            for entry in entries:
                print(f"  - {entry['source_file']}: {entry['id']}")
        else:
            print(f"UNIQUE: {title}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Script to check actual content of target articles
"""

import json

def main():
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
    
    # Target articles to check
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
    
    for target_title in target_titles:
        print(f"\n=== {target_title} ===")
        found = False
        
        for article in articles:
            if article.get('title', '').strip() == target_title:
                found = True
                content = article.get('content', '')
                print(f"Found in: {article['source_file']}")
                print(f"ID: {article.get('id')}")
                print(f"Content length: {len(content)}")
                print("Last 500 characters:")
                print(content[-500:])
                print("\n" + "="*50)
                break
        
        if not found:
            print("NOT FOUND")

if __name__ == '__main__':
    main()

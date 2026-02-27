#!/usr/bin/env python3
"""
Detailed inspection of specific articles to verify deletions
"""

import json

def inspect_article(title, articles):
    """Inspect a specific article"""
    matches = []
    
    for article in articles:
        if article.get('title', '').strip() == title:
            matches.append(article)
    
    return matches

def main():
    print("=== DETAILED ARTICLE INSPECTION ===\n")
    
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
    
    # Check specific articles mentioned in οδηγίες.txt
    target_articles = [
        "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα! Ξεκινάμε ΣΗΜΕΡΑ",
        "Φυσικά Αφροδισιακά για άνδρες και γυναίκες",
        "Umami και…χάνουμε βάρος, τρώγοντας περισσότερο !!!",
        "Κάνοντας Δίαιτα…. παχαίνετε !!!!",
        "Φρούτα, τα οφέλη και οι αντιθέσεις τους"
    ]
    
    for target_title in target_articles:
        print(f"=== INSPECTING: {target_title} ===")
        matches = inspect_article(target_title, articles)
        
        if not matches:
            print("❌ ARTICLE NOT FOUND")
            continue
        
        for i, article in enumerate(matches, 1):
            content = article.get('content', '')
            source = article.get('source_file')
            
            print(f"Version {i} ({source}):")
            print(f"Content length: {len(content)}")
            
            # Check for specific phrases from οδηγίες.txt
            specific_checks = [
                ("Μιλήστε μαζί μας", "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!"),
                ("Συμβουλές/Προτάσεις", "Συμβουλές/Προτάσεις:"),
                ("Τεχνολογία Βιοσυντονισμού", "Τεχνολογία Βιοσυντονισμού"),
                ("Sensitiv Imago", "Sensitiv Imago"),
                ("6975 301223", "6975 301223"),
                ("mistrioti@gmail.com", "mistrioti@gmail.com"),
                ("TERRA PAPERS", "TERRA PAPERS"),
                ("Ετικέτες Diet Coaching", "Ετικέτες Diet Coaching")
            ]
            
            print("Checking for specific phrases:")
            for check_name, phrase in specific_checks:
                if phrase in content:
                    print(f"  ❌ FOUND: {check_name}")
                    # Show context
                    start_pos = content.find(phrase)
                    if start_pos != -1:
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(content), start_pos + len(phrase) + 50)
                        context = content[context_start:context_end]
                        print(f"     Context: ...{context}...")
                else:
                    print(f"  ✅ NOT FOUND: {check_name}")
            
            # Show last 300 characters
            print(f"Last 300 characters:")
            print(content[-300:].replace('\n', ' '))
            print()
    
    print("=== INSPECTION COMPLETE ===")

if __name__ == '__main__':
    main()

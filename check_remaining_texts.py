#!/usr/bin/env python3
"""
Check what texts remain in the articles that should be deleted
"""

import json

def main():
    print("=== CHECKING REMAINING TEXTS ===\n")
    
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
    
    # Key phrases to search for from οδηγίες.txt
    key_phrases = [
        "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!",
        "Συμβουλές/Προτάσεις:",
        "Τεχνολογία Βιοσυντονισμού",
        "Sensitiv Imago",
        "6975 301223",
        "mistrioti@gmail.com",
        "k.mistrioti@yahoo.gr",
        "TERRA PAPERS",
        "Ετικέτες Diet Coaching",
        "Ετικέτες Clinical Nutrition",
        "edw hellas",
        "Ο θεράπων κλινικός διατροφολόγος",
        "Κατερίνα Μηστριώτη",
        "κλινική διατροφολόγος",
        "άρθρο που δημοσιεύτηκε στο"
    ]
    
    articles_with_issues = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        
        found_phrases = []
        for phrase in key_phrases:
            if phrase in content:
                found_phrases.append(phrase)
        
        if found_phrases:
            articles_with_issues.append({
                'title': title,
                'id': article.get('id'),
                'source_file': article.get('source_file'),
                'found_phrases': found_phrases,
                'content_preview': content[-300:].replace('\n', ' ')
            })
    
    print(f"Found {len(articles_with_issues)} articles with remaining texts:")
    
    for i, article in enumerate(articles_with_issues, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source_file']}")
        print(f"   Found phrases: {', '.join(article['found_phrases'])}")
        print(f"   Content preview: {article['content_preview']}")
    
    # Save detailed report
    report = {
        'articles_with_remaining_texts': articles_with_issues,
        'total_articles_with_issues': len(articles_with_issues),
        'timestamp': '2025-02-27T07:10:00Z'
    }
    
    with open('remaining_texts_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nDetailed report saved to remaining_texts_report.json")

if __name__ == '__main__':
    main()

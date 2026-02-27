#!/usr/bin/env python3
"""
Check the Umami article for remaining text
"""

import json

def main():
    print("=== CHECKING UMAMI ARTICLE ===\n")
    
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
    
    # Find Umami article
    target_title = "Umami και…χάνεται βάρος, τρώγοντας περισσότερο !!!"
    
    for article in articles:
        title = article.get('title', '').strip()
        if "Umami" in title and "βάρος" in title:
            print(f"Found: {title}")
            print(f"Source: {article['source_file']}")
            print(f"ID: {article['id']}")
            
            content = article.get('content', '')
            
            # Look for the specific patterns mentioned
            patterns_to_find = [
                "Πρόταση: Τακτικός – ανά τρίμηνο – έλεγχος κατάστασης της υγείας-διατροφικών ελλείψεων και μεταβολισμού – ολόκληρου του οργανισμού με",
                "προσφέρει την δυνατότητα να έχουμε πλήρη εικόνα της υγείας",
                "Η μέθοδος είναι εξαιρετικά οικονομική, μη επεμβατική, ανώδυνη, ακίνδυνη ακόμη και σε παιδιά",
                "60 – 90 λεπτά της ώρας"
            ]
            
            print(f"\nContent length: {len(content)}")
            print(f"\nSearching for patterns:")
            
            for pattern in patterns_to_find:
                if pattern in content:
                    print(f"✅ FOUND: {pattern}")
                    # Show context
                    start_pos = content.find(pattern)
                    if start_pos != -1:
                        context_start = max(0, start_pos - 100)
                        context_end = min(len(content), start_pos + len(pattern) + 100)
                        context = content[context_start:context_end]
                        print(f"   Context: ...{context}...")
                else:
                    print(f"❌ NOT FOUND: {pattern}")
            
            # Show last 500 characters
            print(f"\nLast 500 characters:")
            print(content[-500:])
            
            break
    else:
        print("Umami article not found!")

if __name__ == '__main__':
    main()

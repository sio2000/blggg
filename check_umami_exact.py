#!/usr/bin/env python3
"""
Check the exact content of Umami article
"""

import json

def main():
    print("=== CHECKING UMAMI ARTICLE EXACT CONTENT ===\n")
    
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
    target_title = "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!"
    
    for article in articles:
        title = article.get('title', '').strip()
        if title == target_title:
            print(f"Found: {title}")
            print(f"Source: {article['source_file']}")
            print(f"ID: {article['id']}")
            
            content = article.get('content', '')
            
            # Look for the problematic text
            problematic_text = "Πρόταση:  Τακτικός – ανά τρίμηνο - έλεγχος κατάστασης της υγείας-διατροφικών ελλείψεων και μεταβολισμού - ολοκλήρου του οργανισμού με  «» από την ."
            
            if problematic_text in content:
                print(f"✅ FOUND PROBLEMATIC TEXT: {problematic_text}")
                # Show context
                start_pos = content.find(problematic_text)
                context_start = max(0, start_pos - 100)
                context_end = min(len(content), start_pos + len(problematic_text) + 100)
                context = content[context_start:context_end]
                print(f"Context: ...{context}...")
            else:
                print(f"❌ PROBLEMATIC TEXT NOT FOUND")
                
                # Look for similar patterns
                similar_patterns = [
                    "Πρόταση:",
                    "Τακτικός – ανά τρίμηνο",
                    "«» από την",
                    "ολοκλήρου του οργανισμού με"
                ]
                
                for pattern in similar_patterns:
                    if pattern in content:
                        print(f"✅ FOUND SIMILAR: {pattern}")
                        start_pos = content.find(pattern)
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(content), start_pos + len(pattern) + 50)
                        context = content[context_start:context_end]
                        print(f"  Context: ...{context}...")
            
            # Show last 500 characters
            print(f"\nLast 500 characters:")
            print(content[-500:])
            
            break
    else:
        print("Umami article not found!")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Debug specific article content to see what's actually there
"""

import json

def main():
    print("=== DEBUGGING ARTICLE CONTENT ===\n")
    
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
    
    # Check the "Κάθε μέρα είναι μια νέα ευκαιρία..." article
    target_title = "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!"
    
    for article in articles:
        title = article.get('title', '').strip()
        if title == target_title:
            print(f"Found: {title}")
            print(f"Source: {article['source_file']}")
            print(f"ID: {article['id']}")
            
            content = article.get('content', '')
            print(f"Content length: {len(content)}")
            
            # Look for the specific text
            target_text = "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!"
            
            if target_text in content:
                print(f"✅ FOUND TARGET TEXT: {target_text}")
                # Show context
                start_pos = content.find(target_text)
                context_start = max(0, start_pos - 100)
                context_end = min(len(content), start_pos + len(target_text) + 100)
                context = content[context_start:context_end]
                print(f"Context: ...{context}...")
            else:
                print(f"❌ TARGET TEXT NOT FOUND: {target_text}")
                
                # Look for similar phrases
                similar_phrases = [
                    "Μιλήστε μαζί μας",
                    "βοήθεια που χρειάζεστε",
                    "χρειάζεστε!!!"
                ]
                
                for phrase in similar_phrases:
                    if phrase in content:
                        print(f"✅ FOUND SIMILAR: {phrase}")
                        start_pos = content.find(phrase)
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(content), start_pos + len(phrase) + 50)
                        context = content[context_start:context_end]
                        print(f"  Context: ...{context}...")
            
            # Show last 500 characters
            print(f"\nLast 500 characters:")
            print(content[-500:])
            
            # Also check for any contact information
            contact_patterns = ["6975", "301223", "mistrioti", "gmail", "yahoo"]
            print(f"\nContact information search:")
            for pattern in contact_patterns:
                if pattern in content.lower():
                    print(f"  ✅ Found: {pattern}")
            
            break
    else:
        print("Article not found!")

if __name__ == '__main__':
    main()

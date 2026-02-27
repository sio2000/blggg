#!/usr/bin/env python3
"""
Script to find the 2 articles that should be deleted completely
"""

import json

def main():
    print("=== SEARCHING FOR 2 ARTICLES TO DELETE ===\n")
    
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
    
    # Search for articles containing key words
    target_keywords = [
        ["μόρφωση", "Εναλλακτική Ιατρική"],
        ["Προβιοτικά", "στήθος"]
    ]
    
    found_articles = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        
        for keywords in target_keywords:
            if all(keyword.lower() in title.lower() for keyword in keywords):
                found_articles.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'match_type': 'TITLE'
                })
            elif all(keyword.lower() in content.lower() for keyword in keywords):
                found_articles.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'match_type': 'CONTENT'
                })
    
    print(f"Found {len(found_articles)} matching articles:")
    for article in found_articles:
        print(f"\nTitle: {article['title']}")
        print(f"ID: {article['id']}")
        print(f"Source: {article['source_file']}")
        print(f"Match type: {article['match_type']}")
    
    # Also search for exact titles
    exact_titles = [
        "Τα άτομα με υψηλότερη μόρφωση (ή ανώτερο πνευματικό επίπεδο) είναι ενήμερα για την Εναλλακτική Ιατρική",
        "Προβιοτικά …και για το στήθος !!!!"
    ]
    
    print(f"\n=== SEARCHING FOR EXACT TITLES ===")
    for exact_title in exact_titles:
        found = False
        for article in articles:
            if article.get('title', '').strip() == exact_title:
                found = True
                print(f"FOUND: {exact_title}")
                print(f"  ID: {article.get('id')}")
                print(f"  Source: {article.get('source_file')}")
                break
        if not found:
            print(f"NOT FOUND: {exact_title}")
    
    # Show all article titles for manual inspection
    print(f"\n=== ALL ARTICLE TITLES ===")
    all_titles = [article.get('title', '').strip() for article in articles]
    all_titles.sort()
    
    for i, title in enumerate(all_titles, 1):
        if any(keyword in title.lower() for keywords in target_keywords for keyword in keywords):
            print(f"*** {i}. {title}")
        else:
            print(f"    {i}. {title}")

if __name__ == '__main__':
    main()

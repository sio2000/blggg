#!/usr/bin/env python3
"""
Get the Umami article content from the legacy file restored from git
"""

import json

def main():
    print("=== GETTING LEGACY UMAMI CONTENT ===\n")
    
    # Load the legacy content from git-restored file
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
    
    # Find the Umami article
    target_title = "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!"
    
    for article in legacy_articles:
        title = article.get('title', '').strip()
        if title == target_title:
            print(f"Found: {title}")
            print(f"ID: {article.get('id')}")
            print(f"Published: {article.get('published')}")
            print(f"Updated: {article.get('updated')}")
            
            content = article.get('content', '')
            print(f"Content length: {len(content)}")
            
            # Show first 500 characters
            print(f"\nFirst 500 characters:")
            print(content[:500])
            
            # Show last 500 characters
            print(f"\nLast 500 characters:")
            print(content[-500:])
            
            # Save this content to a file for reference
            with open('umami_original_content.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\nSaved original content to umami_original_content.html")
            
            return article
    
    print("Umami article not found in legacy content!")
    return None

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Manual script to upload articles to Netlify
This script will read your local articles and upload them to your Netlify site
"""

import json
import requests
import time
import sys
from pathlib import Path

def load_local_articles():
    """Load articles from .data/articles.json"""
    try:
        with open('.data/articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"✓ Loaded {len(articles)} articles from .data/articles.json")
        return articles
    except FileNotFoundError:
        print("✗ Error: .data/articles.json not found")
        print("Make sure you're running this script from the blog2 directory")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing .data/articles.json: {e}")
        sys.exit(1)

def upload_articles_to_netlify(articles, netlify_url):
    """Upload articles to Netlify via API"""
    print(f"\nStarting upload to: {netlify_url}")
    print("=" * 50)
    
    success_count = 0
    failed_count = 0
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] {article['title'][:60]}...")
        
        try:
            # Prepare the payload
            payload = {
                'title': article['title'],
                'content': article['content'],
                'imageUrl': article.get('imageUrl'),
                'author': article.get('author', 'Katerina Mistrioti'),
                'labels': article.get('labels', []),
                'category': article.get('category', 'Αρχική σελίδα')
            }
            
            # Make the API request
            response = requests.post(
                f"{netlify_url}/api/articles",
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print(f"  ✓ Success")
                success_count += 1
            else:
                print(f"  ✗ Failed - HTTP {response.status_code}")
                if response.text:
                    print(f"    Error: {response.text[:200]}...")
                failed_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Network error: {e}")
            failed_count += 1
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            failed_count += 1
        
        # Rate limiting - be nice to the server
        time.sleep(0.5)
    
    return success_count, failed_count

def main():
    print("=== Netlify Article Upload Tool ===\n")
    
    # Load articles
    articles = load_local_articles()
    if not articles:
        print("No articles to upload. Exiting.")
        return
    
    # Try different Netlify URLs
    netlify_urls = [
        "https://your-blog-name.netlify.app",  # REPLACE WITH YOUR ACTUAL NETLIFY URL
        "https://your-site.netlify.app",       # Alternative
    ]
    
    # For testing, you can also use localhost
    test_local = input("Test with localhost first? (y/n): ").lower().strip()
    
    if test_local == 'y':
        netlify_urls.insert(0, "http://localhost:3000")
    
    print("\nAvailable targets:")
    for i, url in enumerate(netlify_urls, 1):
        print(f"{i}. {url}")
    
    choice = input(f"\nSelect target (1-{len(netlify_urls)}) or enter custom URL: ").strip()
    
    try:
        if choice.isdigit():
            target_url = netlify_urls[int(choice) - 1]
        else:
            target_url = choice
    except:
        print("Invalid choice. Exiting.")
        return
    
    print(f"\nTarget: {target_url}")
    confirm = input("Proceed with upload? (y/n): ").lower().strip()
    
    if confirm != 'y':
        print("Upload cancelled.")
        return
    
    # Perform the upload
    success, failed = upload_articles_to_netlify(articles, target_url)
    
    print("\n" + "=" * 50)
    print("UPLOAD COMPLETE")
    print("=" * 50)
    print(f"✓ Successfully uploaded: {success} articles")
    print(f"✗ Failed to upload: {failed} articles")
    
    if failed == 0:
        print("\n🎉 All articles uploaded successfully!")
        print("Please check your Netlify site to verify all articles are visible.")
    else:
        print(f"\n⚠️  {failed} articles failed to upload.")
        print("Please check the errors above and try again.")

if __name__ == '__main__':
    main()

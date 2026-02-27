#!/usr/bin/env python3
"""
Script to scrape articles from diet-web.blogspot.com and convert to database format
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

def scrape_article(url):
    """Scrape a single article from Blogspot URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content area
        content_div = soup.find('div', class_='post-body')
        if not content_div:
            content_div = soup.find('div', {'class': 'post-body entry-content'})
        
        # Extract title
        title_elem = soup.find('h3', class_='post-title') or soup.find('h1', class_='post-title')
        title = title_elem.get_text(strip=True) if title_elem else "Untitled"
        
        # Extract date
        date_elem = soup.find('h2', class_='date-header') or soup.find('span', class_='date-header')
        date_str = date_elem.get_text(strip=True) if date_elem else ""
        
        # Extract content and images
        content_html = str(content_div) if content_div else ""
        
        # Find all images
        images = []
        if content_div:
            img_tags = content_div.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if src and not src.startswith('data:'):
                    # Convert blogspot images to full size
                    if 'blogspot.com' in src and '/s' in src:
                        src = re.sub(r'/s\d+-c/', '/s1600/', src)
                        src = re.sub(r'/s\d+/', '/s1600/', src)
                    images.append(src)
        
        # Clean up content
        content_html = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content_html)
        
        # Generate unique ID
        post_id = f"diet-web-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(url) % 10000}"
        
        article = {
            "id": post_id,
            "title": title,
            "content": content_html,
            "imageUrl": images[0] if images else None,
            "author": "Katerina Mistrioti",
            "published": date_str,
            "labels": [],
            "category": "Αρχική σελίδα",
            "source_url": url
        }
        
        return article
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    # URLs to scrape
    urls = [
        "https://diet-web.blogspot.com/2014/02/blog-post_25.html",
        "https://diet-web.blogspot.com/2014/02/blog-post.html", 
        "https://diet-web.blogspot.com/2014/02/4-2-4-2.html",
        "https://diet-web.blogspot.com/2014/03/blog-post_13.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_28.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_7.html",
        "https://diet-web.blogspot.com/2015/04/blog-post_20.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_9370.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_27.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_7832.html",
        "https://diet-web.blogspot.com/2014/02/blog-post_4453.html"
    ]
    
    # Remove duplicates
    urls = list(set(urls))
    
    articles = []
    
    for url in urls:
        print(f"Scraping: {url}")
        article = scrape_article(url)
        if article:
            articles.append(article)
            print(f"  ✓ Scraped: {article['title']}")
        else:
            print(f"  ✗ Failed to scrape")
        
        # Be respectful to the server
        time.sleep(1)
    
    # Save to JSON file
    with open('scraped_articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"\nScraped {len(articles)} articles successfully!")
    print("Saved to scraped_articles.json")
    
    # Also create API insertion script
    create_api_script(articles)

def create_api_script(articles):
    """Create a script to insert articles via API"""
    script_content = '''#!/usr/bin/env python3
"""
Script to insert scraped articles into the database via API
"""

import requests
import json

def insert_article(article):
    """Insert a single article via API"""
    try:
        response = requests.post('http://localhost:3000/api/articles', json={
            'title': article['title'],
            'content': article['content'],
            'imageUrl': article['imageUrl'],
            'author': article['author'],
            'labels': article['labels'],
            'category': article['category']
        })
        
        if response.status_code == 201:
            print(f"✓ Inserted: {article['title']}")
            return True
        else:
            print(f"✗ Failed to insert: {article['title']} - {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error inserting {article['title']}: {e}")
        return False

def main():
    # Load scraped articles
    with open('scraped_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"Inserting {len(articles)} articles...")
    
    success_count = 0
    for article in articles:
        if insert_article(article):
            success_count += 1
    
    print(f"\\nSuccessfully inserted {success_count}/{len(articles)} articles")

if __name__ == '__main__':
    main()
'''
    
    with open('insert_articles.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Created insert_articles.py for API insertion")

if __name__ == '__main__':
    main()

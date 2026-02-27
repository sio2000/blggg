#!/usr/bin/env python3
"""
Detailed check of all 17 articles to verify text deletions
"""

import json

def load_articles():
    """Load articles from both sources"""
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
    
    return articles

def check_article_content(title, articles):
    """Check specific article content"""
    matches = []
    
    for article in articles:
        if article.get('title', '').strip() == title:
            matches.append(article)
    
    return matches

def main():
    print("=== DETAILED CHECK OF 17 ARTICLES ===\n")
    
    articles = load_articles()
    
    # The 17 target articles
    target_articles = [
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
    
    # Text patterns that should NOT exist anymore
    forbidden_patterns = [
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
        "Ο θεράπων κλινικός διατροφολόγος"
    ]
    
    issues_found = []
    
    for title in target_articles:
        print(f"=== CHECKING: {title} ===")
        matches = check_article_content(title, articles)
        
        if not matches:
            print("❌ ARTICLE NOT FOUND")
            continue
        
        for i, article in enumerate(matches, 1):
            content = article.get('content', '')
            source = article.get('source_file')
            
            print(f"Version {i} ({source}):")
            
            # Check for forbidden patterns
            found_patterns = []
            for pattern in forbidden_patterns:
                if pattern in content:
                    found_patterns.append(pattern)
            
            if found_patterns:
                print(f"❌ FOUND FORBIDDEN PATTERNS: {', '.join(found_patterns)}")
                issues_found.append({
                    'title': title,
                    'source': source,
                    'patterns': found_patterns
                })
                
                # Show context around found patterns
                for pattern in found_patterns:
                    start_pos = content.find(pattern)
                    if start_pos != -1:
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(content), start_pos + len(pattern) + 50)
                        context = content[context_start:context_end]
                        print(f"   Context: ...{context}...")
            else:
                print("✅ NO FORBIDDEN PATTERNS FOUND")
            
            # Show last 200 characters of content for manual verification
            print(f"   Last 200 chars: {content[-200:].replace(chr(10), ' ')}")
            print()
    
    # Summary
    print("=== SUMMARY ===")
    if issues_found:
        print(f"❌ Found {len(issues_found)} articles with remaining forbidden patterns:")
        for issue in issues_found:
            print(f"  - {issue['title']} ({issue['source']}): {', '.join(issue['patterns'])}")
    else:
        print("✅ ALL ARTICLES CLEAN - No forbidden patterns found!")
    
    return len(issues_found) == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

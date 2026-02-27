#!/usr/bin/env python3
"""
Final verification of all changes
"""

import json
import os

def main():
    print("=== FINAL VERIFICATION ===\n")
    
    # Load current articles
    current_articles = []
    
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
        for article in db_articles:
            article['source_file'] = '.data/articles.json'
            current_articles.append(article)
    
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
        for article in legacy_articles:
            article['source_file'] = 'src/lib/content.json'
            current_articles.append(article)
    
    print(f"Current total articles: {len(current_articles)}")
    print(f"Database articles: {len(db_articles)}")
    print(f"Legacy articles: {len(legacy_articles)}")
    
    # Check deleted articles
    deleted_titles = [
        "Τα άτομα με υψηλότερη μόρφωση  (ή ανώτερο πνευματικό επίπεδο) είναι ενμένα για την Εναλλακτική Ιατρική",
        "Προβιοτικά …και για το στήθος !!!!"
    ]
    
    print("\n=== VERIFYING DELETED ARTICLES ===")
    for deleted_title in deleted_titles:
        found = False
        for article in current_articles:
            if article.get('title', '').strip() == deleted_title:
                found = True
                print(f"❌ STILL EXISTS: {deleted_title}")
                break
        if not found:
            print(f"✅ SUCCESSFULLY DELETED: {deleted_title}")
    
    # Check specific text deletions
    print("\n=== VERIFYING TEXT DELETIONS ===")
    
    # Text patterns that should be deleted
    deleted_patterns = [
        "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!",
        "Sensitiv Imago",
        "Τεχνολογία Βιοσυντονισμού",
        "Ελάτε να φτιάξουμε ένα πρόγραμμα",
        "Επικοινωνήστε μαζί μου",
        "6975 301223",
        "mistrioti@gmail.com",
        "k.mistrioti@yahoo.gr",
        "terra papers",
        "edw hellas",
        "Ετικέτες Diet Coaching",
        "Ετικέτες Clinical Nutrition"
    ]
    
    verification_results = []
    
    for article in current_articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        
        found_patterns = []
        for pattern in deleted_patterns:
            if pattern.lower() in content.lower():
                found_patterns.append(pattern)
        
        if found_patterns:
            verification_results.append({
                'title': title,
                'id': article.get('id'),
                'source_file': article.get('source_file'),
                'found_patterns': found_patterns
            })
    
    if verification_results:
        print(f"❌ Found {len(verification_results)} articles with deleted patterns still present:")
        for result in verification_results:
            print(f"\n  Article: {result['title']}")
            print(f"  Source: {result['source_file']}")
            print(f"  Patterns found: {', '.join(result['found_patterns'])}")
    else:
        print("✅ SUCCESS: All deleted patterns have been removed!")
    
    # Check for broken HTML structure
    print("\n=== VERIFYING HTML STRUCTURE ===")
    html_issues = []
    
    for article in current_articles:
        content = article.get('content', '')
        title = article.get('title', '').strip()
        
        # Check for unclosed tags
        open_divs = content.count('<div') - content.count('</div>')
        open_divs_style = content.count("<div") - content.count("</div>")
        
        if open_divs != 0 or open_divs_style != 0:
            html_issues.append({
                'title': title,
                'issue': f'Unmatched div tags: {open_divs}'
            })
    
    if html_issues:
        print(f"❌ Found {len(html_issues)} articles with HTML issues:")
        for issue in html_issues:
            print(f"  - {issue['title']}: {issue['issue']}")
    else:
        print("✅ SUCCESS: No HTML structure issues found!")
    
    # Summary report
    print("\n=== FINAL SUMMARY ===")
    
    # Load deletion reports
    try:
        with open('smart_deletion_report.json', 'r', encoding='utf-8') as f:
            smart_report = json.load(f)
        
        with open('final_deletion_report.json', 'r', encoding='utf-8') as f:
            complete_report = json.load(f)
        
        total_text_deletions = len(smart_report.get('changes_made', []))
        total_complete_deletions = len(complete_report.get('complete_deletions', []))
        
        print(f"Text deletions applied: {total_text_deletions}")
        print(f"Complete article deletions: {total_complete_deletions}")
        print(f"Total operations: {total_text_deletions + total_complete_deletions}")
        
    except Exception as e:
        print(f"Could not load reports: {e}")
    
    print(f"\nFinal article count: {len(current_articles)}")
    print(f"Articles with remaining issues: {len(verification_results) + len(html_issues)}")
    
    # Save final verification report
    final_report = {
        'verification_timestamp': '2025-02-27T06:45:00Z',
        'total_articles': len(current_articles),
        'database_articles': len(db_articles),
        'legacy_articles': len(legacy_articles),
        'articles_with_remaining_patterns': len(verification_results),
        'html_structure_issues': len(html_issues),
        'verification_results': verification_results,
        'html_issues': html_issues,
        'status': 'COMPLETED' if len(verification_results) == 0 and len(html_issues) == 0 else 'NEEDS_REVIEW'
    }
    
    with open('final_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal verification report saved to final_verification_report.json")

if __name__ == '__main__':
    main()

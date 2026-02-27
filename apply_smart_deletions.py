#!/usr/bin/env python3
"""
Script to apply smart text deletions using pattern matching
"""

import json
import re
import os

def load_articles():
    """Load articles from both sources"""
    articles = []
    
    # Load from .data/articles.json (database)
    with open('.data/articles.json', 'r', encoding='utf-8') as f:
        db_articles = json.load(f)
        for article in db_articles:
            article['source_file'] = '.data/articles.json'
            articles.append(article)
    
    # Load from src/lib/content.json (legacy)
    with open('src/lib/content.json', 'r', encoding='utf-8') as f:
        content_data = json.load(f)
        legacy_articles = content_data.get('posts', [])
        for article in legacy_articles:
            article['source_file'] = 'src/lib/content.json'
            articles.append(article)
    
    return articles

def apply_smart_deletions(articles):
    """Apply smart deletions using pattern matching"""
    
    changes_made = []
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Define patterns to search and delete
        patterns = []
        
        if title == "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα! Ξεκινάμε ΣΗΜΕΡΑ":
            patterns = [
                r"Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!",
                r"Μιλήστε μαζί μας.*?χρειάζεστε!!!"
            ]
        
        elif title == "Φυσικά Αφροδισιακά για άνδρες και γυναίκες":
            patterns = [
                r"Συμβουλές/Προτάσεις:.*?Sensitiv\s*Imago.*?Ετικέτες\s*Diet Coaching",
                r"Τεχνολογία Βιοσυντονισμού.*?Sensitiv Imago.*?60 – 90 λεπτά.*?Sensitiv Imago",
                r"Τεχνολογία Βιοσυντονισμού.*?πριν εκδηλωθούν.*?Sensitiv Imago"
            ]
        
        elif title == "Umami και…χάνουμε βάρος, τρώγοντας περισσότερο !!!":
            patterns = [
                r"Πρόταση:.*?Sensitiv\s*Imago.*?60 – 90 λεπτά.*?Sensitiv Imago",
                r"Τεχνολογία Βιοσυντονισμού.*?Umami.*?Sensitiv Imago"
            ]
        
        elif title == "Κάνοντας Δίαιτα…. παχαίνετε !!!!":
            patterns = [
                r"Έλεγχος με το.*?Sensitiv\s*Imago.*?αναλόγως\.",
                r"Έλεγχος με το.*?Διατροφής.*?αναλόγως"
            ]
        
        elif title == "Φρούτα, τα οφέλη και οι αντιθέσεις τους":
            patterns = [
                r"Κατερίνα Μυστριώτη:.*?Ετικέτες\s*Diet Coaching",
                r"Περισσότερα σχετικά.*?TERRA PAPERS.*?Diet Coaching"
            ]
        
        elif title == "Βιολογικά Προϊόντα Μύθοι και Αλήθειες":
            patterns = [
                r"Κατερίνα Μηστριώτη.*?κλινική διατροφολόγος.*?terra papers.*?Diet Coaching",
                r"άρθρο που δημοσιεύτηκε στο.*?terra papers.*?Diet Coaching"
            ]
        
        elif title == "4 μικρά μυστικά και χάνετε 2-4 κιλά":
            patterns = [
                r"Ελάτε να φτιάξουμε.*?mistrioti@gmail\.com.*?Diet Coaching",
                r"Επικοινωνήστε μαζί μου.*?6975 301223.*?Diet Coaching"
            ]
        
        elif title == "Τροφές που μπλοκάρουν την απώλεια κιλών":
            patterns = [
                r"Κατερίνα Μηστριώτη.*?Κλινική Διατροφόλογος.*?terra papers.*?Diet Coaching",
                r"Άρθρο που δημοσιεύτηκε στο.*?terra papers.*?Diet Coaching"
            ]
        
        elif title == "Αδυνατείστε με υδατάνθρακες":
            patterns = [
                r"Ελάτε να φτιάξουμε.*?k\.mistrioti@yahoo\.gr.*?Diet Coaching",
                r"Επικοινωνήστε μαζί μου.*?6975 301223.*?Diet Coaching"
            ]
        
        elif title == "Η σεροτονίνη φέρνει ευτυχία κι επιτυχία":
            patterns = [
                r"Κατερίνα Μηστριώτη.*?κλινική διατροφολόγος.*?terra papers.*?Clinical Nutrition",
                r"Η σεροτονίνη φέρνει ευτυχία.*?terra papers.*?Clinical Nutrition"
            ]
        
        elif title == "Μαγγάνιο το πολύτιμο μέταλλο":
            patterns = [
                r"Άρθρο που δημοσιεύτηκε στο.*?edwhellas\.gr.*?terrapapers\.com.*?Clinical Nutrition",
                r"edwhellas\.gr.*?terrapapers\.com.*?Clinical Nutrition"
            ]
        
        elif title == "Το σωσίβιο είναι επικίνδυνο":
            patterns = [
                r"Ο Διατροφολόγος σας.*?Sensitiv Imago.*?αναλόγω\.",
                r"Ο Διατροφολόγος σας.*?Sensitiv Imago.*?Sensitiv Imago"
            ]
        
        elif title == "Το πάχος ξεκινά και ρυθμίζεται από τον εγκέφαλο":
            patterns = [
                r"TERRA PAPERS.*?Ετικέτες\s*Diet Coaching",
                r"TERRA PAPERS.*?Diet Coaching"
            ]
        
        elif title == "Η Διατροφή κατα της γρίπης":
            patterns = [
                r"Επικοινώνησε μαζί μου.*?k\.mistrioti@yahoo\.gr.*?Diet Coaching",
                r"6975 301223.*?k\.mistrioti@yahoo\.gr.*?Diet Coaching"
            ]
        
        elif title == "Λεπτίνη, η ορμόνη ρυθμιστής της Ενέργειας":
            patterns = [
                r"Κατερίνα Μηστριώτη.*?κλινική διατροφολόγος.*?terra papers.*?$",
                r'"Λεπτίνη.*?Ενέργειας".*?terra papers.*?$'
            ]
        
        elif title == "Παραμείνετε λεπτοί χωρίς δίαιτα":
            patterns = [
                r"edw hellas",
                r"Ο θεράπων κλινικός διατροφολόγος.*?γι' αυτόν\."
            ]
        
        # Apply patterns
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                content = content.replace(match, '')
                changes_made.append({
                    'title': title,
                    'id': article.get('id'),
                    'source_file': article.get('source_file'),
                    'action': 'TEXT_DELETED',
                    'deleted_text': match[:100] + '...' if len(match) > 100 else match
                })
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = content.strip()
        
        if content != original_content:
            article['content'] = content
    
    # Handle complete deletions
    delete_completely = [
        "Τα άτομα με υψηλότερη μόρφωση (ή ανώτερο πνευματικό επίπεδο) είναι ενήμερα για την Εναλλακτική Ιατρική",
        "Προβιοτικά …και για το στήθος !!!!"
    ]
    
    for article in articles:
        title = article.get('title', '').strip()
        if title in delete_completely:
            article['content'] = "[DELETED]"
            changes_made.append({
                'title': title,
                'id': article.get('id'),
                'source_file': article.get('source_file'),
                'action': 'DELETED_COMPLETELY'
            })
    
    return articles, changes_made

def save_articles(articles):
    """Save articles back to their respective files"""
    
    # Separate by source file
    db_articles = []
    legacy_articles = []
    
    for article in articles:
        if article.get('source_file') == '.data/articles.json':
            db_articles.append(article)
        elif article.get('source_file') == 'src/lib/content.json':
            # Remove the extra fields for legacy format
            legacy_article = {
                'id': article.get('id'),
                'published': article.get('published'),
                'updated': article.get('updated'),
                'title': article.get('title'),
                'content': article.get('content'),
                'labels': article.get('labels', []),
                'link': article.get('link', ''),
                'author': article.get('author')
            }
            legacy_articles.append(legacy_article)
    
    # Save database articles
    with open('.data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(db_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(db_articles)} articles to .data/articles.json")
    
    # Save legacy articles
    content_data = {
        'posts': legacy_articles
    }
    with open('src/lib/content.json', 'w', encoding='utf-8') as f:
        json.dump(content_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(legacy_articles)} articles to src/lib/content.json")

def main():
    print("=== APPLYING SMART DELETIONS ===\n")
    
    # Load articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Apply deletions
    modified_articles, changes_made = apply_smart_deletions(articles)
    
    # Save changes
    save_articles(modified_articles)
    
    # Report
    print("\n=== DELETION REPORT ===")
    print(f"Total changes made: {len(changes_made)}")
    
    by_action = {}
    for change in changes_made:
        action = change['action']
        if action not in by_action:
            by_action[action] = []
        by_action[action].append(change)
    
    for action, items in by_action.items():
        print(f"\n{action}: {len(items)} articles")
        for item in items:
            print(f"  - {item['title']} ({item['source_file']})")
    
    # Save report
    report = {
        'changes_made': changes_made,
        'total_changes': len(changes_made),
        'timestamp': '2025-02-27T06:30:00Z'
    }
    
    with open('smart_deletion_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nSmart deletion report saved to smart_deletion_report.json")

if __name__ == '__main__':
    main()

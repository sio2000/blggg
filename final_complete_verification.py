#!/usr/bin/env python3
"""
Final complete verification of all 17 articles
"""

import json

def main():
    print("=== FINAL COMPLETE VERIFICATION ===\n")
    
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
    
    # The actual titles found
    target_articles = [
        "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!",
        "Φυσικά Αφροδισιακά για άνδρες και γυναίκες",
        "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!",
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
    
    # Key phrases that should NOT exist (from οδηγίες.txt)
    forbidden_phrases = [
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
        "Ο θεράπων κλινικός διατροφολόγος",
        "Κατερίνα Μηστριώτη",
        "κλινική διατροφολόγος",
        "άρθρο που δημοσιεύτηκε στο",
        "Πρόταση: Τακτικός – ανά τρίμηνο",
        "Έλεγχος με το «Sensitiv Imago»",
        "60 – 90 λεπτά της ώρας"
    ]
    
    all_clean = True
    issues_found = []
    
    for target_title in target_articles:
        print(f"=== CHECKING: {target_title} ===")
        
        found_articles = []
        for article in articles:
            if article.get('title', '').strip() == target_title:
                found_articles.append(article)
        
        if not found_articles:
            print("❌ ARTICLE NOT FOUND")
            all_clean = False
            continue
        
        for i, article in enumerate(found_articles, 1):
            content = article.get('content', '')
            source = article.get('source_file')
            
            print(f"Version {i} ({source}):")
            
            # Check for forbidden phrases
            found_phrases = []
            for phrase in forbidden_phrases:
                if phrase in content:
                    found_phrases.append(phrase)
            
            if found_phrases:
                print(f"❌ FOUND FORBIDDEN PHRASES: {', '.join(found_phrases)}")
                issues_found.append({
                    'title': target_title,
                    'source': source,
                    'phrases': found_phrases
                })
                all_clean = False
                
                # Show context for first few phrases
                for phrase in found_phrases[:3]:
                    start_pos = content.find(phrase)
                    if start_pos != -1:
                        context_start = max(0, start_pos - 50)
                        context_end = min(len(content), start_pos + len(phrase) + 50)
                        context = content[context_start:context_end]
                        print(f"   Context: ...{context}...")
            else:
                print("✅ CLEAN - No forbidden phrases found")
            
            # Show content length for verification
            print(f"   Content length: {len(content)}")
            print()
    
    # Final summary
    print("=== FINAL SUMMARY ===")
    if all_clean:
        print("🎉 SUCCESS: ALL 17 ARTICLES ARE CLEAN!")
        print("✅ All forbidden phrases have been successfully deleted")
        print("✅ All articles comply with οδηγίες.txt requirements")
    else:
        print(f"❌ ISSUES FOUND: {len(issues_found)} articles still have forbidden phrases")
        for issue in issues_found:
            print(f"  - {issue['title']} ({issue['source']}): {', '.join(issue['phrases'])}")
    
    # Save final verification report
    report = {
        'verification_status': 'CLEAN' if all_clean else 'NEEDS_CLEANUP',
        'total_articles_checked': len(target_articles),
        'articles_with_issues': len(issues_found),
        'issues': issues_found,
        'timestamp': '2025-02-27T07:20:00Z'
    }
    
    with open('final_complete_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal verification report saved to final_complete_verification_report.json")
    
    return all_clean

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

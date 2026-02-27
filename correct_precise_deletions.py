#!/usr/bin/env python3
"""
Correct precise deletions using the actual titles found
"""

import json
import re

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

def apply_correct_precise_deletions(articles):
    """Apply precise deletions using the correct titles"""
    
    changes_made = []
    
    # Use the actual titles found
    deletion_texts = {
        "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!": [
            "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!"
        ],
        
        "Φυσικά Αφροδισιακά για άνδρες και γυναίκες": [
            """Συμβουλές/Προτάσεις:\xa0\xa0\xa0\xa0
Τακτικός – ανά τρίμηνο - έλεγχος κατάστασης της Υγείας-Διατροφικών ελλείψεων και Μεταβολισμού - ολοκλήρου του οργανισμού με\xa0\xa0Τεχνολογία Βιοσυντονισμού «Sensitiv\xa0Imago»\xa0*\xa0από την Κατερίνα Μηστριώτη.
*\xa0Η Τεχνολογία Βιοσυντονισμού του\xa0 «Sensitiv Imago»\xa0\xa0προσφέρει την δυνατότητα\xa0να έχουμε πλήρη εικόνα της υγείας, των διατροφικών μας ελλείψεων και της κατάστασης του μεταβολισμού μας και εντοπίζει διαταραχές στο αρχικό στάδιο ακόμη και πριν εκδηλωθούν. \xa0
Τεχνολογία Βιοσυντονισμού\xa0 "Sensitiv Imago"
Η μέθοδος είναι εξαιρετικά οικονομική, μη επεμβατική, ανώδυνη, ακίνδυνη ακόμη και σε παιδιά και ο χρόνος που απαιτείται είναι μόνον 60 – 90 λεπτά της ώρας.
Περισσότερες πληροφορίες για την μέθοδο θα βρείτε στο τμήμα της σελίδας του\xa0blog\xa0που αναφέρεται αποκλειστικά στο\xa0«Sensitiv Imago»."""
        ],
        
        "Umami  και…χάνουμε βάρος,  τρώγοντας περισσότερο !!!": [
            """\xa0\xa0Πρόταση:\xa0 Τακτικός – ανά τρίμηνο - έλεγχος κατάστασης της υγείας-διατροφικών ελλείψεων και μεταβολισμού - ολοκλήρου του οργανισμού με\xa0Τεχνολογία Βιοσυντονισμού «Sensitiv Imago»\xa0από την Κατερίνα Μηστριώτη *
*   Η Τεχνολογία Βιοσυντονισμού του\xa0 «Sensitiv Imago»\xa0\xa0προσφέρει την δυνατότητα\xa0να έχουμε πλήρη εικόνα της υγείας, των διατροφικών μας ελλείψεων και της κατάστασης του μεταβολισμού μας και εντοπίζει διαταραχές στο αρχικό στάδιο ακόμη και πριν εκδηλωθούν. \xa0
\xa0   \xa0 Η μέθοδος είναι εξαιρετικά οικονομική, μη επεμβατική, ανώδυνη, ακίνδυνη ακόμη και σε παιδιά και ο χρόνος που απαιτείται είναι μόνον 60 – 90 λεπτά της ώρας.

   Περισσότερες πληροφορίες για την μέθοδο θα βρείτε στο τμήμα της σελίδας του\xa0blog\xa0που αναφέρεται αποκλειστικά στο\xa0«Sensitiv Imago».\xa0"""
        ],
        
        "Κάνοντας Δίαιτα…. παχαίνετε !!!!": [
            """Έλεγχος με το «Sensitiv\xa0Imago» από τον Διατροφολόγο σας
Ο έλεγχος θα δώσει πολύτιμες πληροφορίες για την παρούσα κατάσταση του οργανισμού σας, ποιες τροφές σας επηρεάζουν, σε ποιες Βιταμίνες και Μέταλλα έχετε έλλειψη, ποια Βαρέα Μέταλλα σε υψηλά επίπεδα σας επιβαρύνουν, εάν υπάρχουν μύκητες και\xa0Candida\xa0η οποία εμποδίζει την σωστή λειτουργία του οργανισμού σας.
Θα ελεγχθεί η ανταπόκριση του μεταβολικού σας συστήματος και η κατάσταση του πεπτικού και εντερικού συστήματος και πολλά άλλα.
Βάσει των αποτελεσμάτων θα συνταχθεί\xa0 αποκλειστικά Ατομική ειδική Διατροφή καθώς επίσης και εξατομικευμένος κατάλογος Συμπληρωμάτων Διατροφής προκειμένου ο οργανισμός να έλθει σε ισορροπία και να ξεκινήσει την σωστή λειτουργία απώλειας λίπους.
Θα γίνει μέτρηση «ΠΣΛ» με τελευταίας τεχνολογίας συσκευές ώστε να γνωρίζετε τα ποσοστά σωματικού λίπους τα οποία είχατε ξεκινώντας και την πορεία της προσπάθειάς σας.
Μετά από 3 μήνες είναι καλό να επαναλάβετε τον έλεγχος ώστε να βεβαιωθείτε για την πρόοδό σας και να προσαρμοστεί το πρόγραμμα Διατροφής και Συμπληρωμάτων Διατροφής, αναλόγως."""
        ],
        
        "Φρούτα, τα οφέλη και οι αντιθέσεις τους": [
            """Κατερίνα Μυστριώτη:\xa0Περισσότερα σχετικά με τους συνδυασμούς και τα οφέλη των τροφών για μια διατροφή υγιεινή που να σου χαρίζει Ενέργεια και Δύναμη επικοινωνήστε μαζί μου στο τηλ.\xa06975 301223\xa010πμ-19μμ ή στείλε μου e-mail:\xa0mistrioti@gmail.com
\xa0\xa0\xa0\xa0\xa0\xa0\xa0 TERRA PAPERS
\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Βιολογικά Προϊόντα Μύθοι και Αλήθειες": [
            """Κατερίνα Μηστριώτη\xa0\xa0\xa0\xa0κλινική διατροφολόγος
\xa0\xa0\xa0\xa0 άρθρο που δημοσιεύτηκε στο\xa0terra papers
\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "4 μικρά μυστικά και χάνετε 2-4 κιλά": [
            """\xa0\xa0Ελάτε να φτιάξουμε ένα πρόγραμμα σωστής και ενεργειακά δυνατής διατροφής για υγεία και ευεξία, απλά επικοινωνήστε μαζί μου, Κατερίνα Μηστριώτη στο τηλ. 6975 301223 (10πμ.-19μ.μ.) και\xa0mistrioti@gmail.com
\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Τροφές που μπλοκάρουν την απώλεια κιλών": [
            """Κατερίνα Μηστριώτη\xa0\xa0\xa0\xa0Κλινική Διατροφόλογος και Σύμβουλος Ολιστικών Εφαρμογών.
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Άρθρο που δημοσιεύτηκε στο terra papers\xa0
\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Αδυνατείστε με υδατάνθρακες": [
            """\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0Ελάτε να φτιάξουμε ένα πρόγραμμα σωστής και ενεργειακά δυνατής διατροφής σε ατομικό επίπεδο, για υγεία και ευεξία. Επικοινωνήστε μαζί μου, Κατερίνα Μηστριώτη στο τηλ. 6975 301223 (10πμ.-19μ.μ.) και k.mistrioti@yahoo.gr
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Η σεροτονίνη φέρνει ευτυχία κι επιτυχία": [
            """Κατερίνα Μηστριώτη\xa0\xa0\xa0\xa0κλινική διατροφολόγος\xa0\xa0Η σεροτονίνη φέρνει ευτυχία κι επιτυχία\xa0άρθρο που δημοσιεύτηκε στο\xa0terra papers
\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Ετικέτες\xa0Clinical Nutrition"""
        ],
        
        "Μαγγάνιο το πολύτιμο μέταλλο": [
            """\xa0\xa0\xa0\xa0\xa0\xa0 Άρθρο που δημοσιεύτηκε στο\xa0edwhellas.gr\xa0και στο\xa0terrapapers.com
\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Ετικέτες\xa0Clinical Nutrition"""
        ],
        
        "Το σωσίβιο είναι επικίνδυνο": [
            """\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0Ο Διατροφολόγος σας είναι εκείνος που μπορεί να σας συμβουλέψει επάνω στα προγράμματα αποκλειστικά προσωπικής Διατροφής, Συμπληρωμάτων Διατροφής και Βοτάνων και είναι καλό να ξεκινήσετε κάνοντας έλεγχο *Sensitiv Imago.
Με τον έλεγχο αυτό θα λάβετε πολύτιμες πληροφορίες για την παρούσα κατάσταση του οργανισμού σας όπως επίσης και ποιες Βιταμίνες, Μέταλλα, Αμινοξέα και άλλα στοιχεία έχετε σε έλλειψη και τα οποία θα μπορούσατε να λάβετε σε συμπληρώματα , προκειμένου ο οργανισμός σας να έλθει και πάλι σε ισορροπία και σωστή λειτουργία. Επίσης θα ελεγχθεί η κατάσταση του πεπτικού σας συστήματος και στην συνέχεια θα ενημερωθείτε για το ποια μέτρα είναι καλό να λάβετε για την αντιμετώπιση των τους και την γενική σας αναδόμηση.
Σε συνεννόηση με τον Διατροφολόγο σας, μετά από 3 μήνες είναι καλό να προχωρήσετε και πάλι σε έλεγχο *Sensitiv Imago για να βεβαιωθείτε για την πρόοδό σας και να προσαρμόσετε το πρόγραμμα διατροφής και συμπληρωμάτων, αναλόγως.
\xa0\xa0\xa0\xa0\xa0\xa0\xa0 Sensitiv Imago"""
        ],
        
        "Το πάχος ξεκινά και ρυθμίζεται από τον εγκέφαλο": [
            """\xa0\xa0\xa0\xa0\xa0\xa0\xa0 TERRA PAPERS
\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Η Διατροφή κατα της γρίπης": [
            """\xa0\xa0Επικοινώνησε μαζί μου να συζητήσουμε ποιές βιταμίνες είναι απαραίτητες για να θωρακίσεις την υγεία σου σε ατομικό επίπεδο στο 6975 301223 και\xa0\xa0k.mistrioti@yahoo.gr
Κατερίνα Μηστριώτη\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0(σύμβουλος κλινικής διατροφολογίας)
Αναρτήθηκε από\xa0Katerina Mistrioti mistrioti@gmail.com\xa0στις\xa07:25\xa0μ.μ.\xa0
\xa0\xa0\xa0\xa0\xa0\xa0 Ετικέτες\xa0Diet Coaching"""
        ],
        
        "Λεπτίνη, η ορμόνη ρυθμιστής της Ενέργειας": [
            """Κατερίνα Μηστριώτη\xa0\xa0κλινική διατροφολόγος και σύμβουλος Ολιστικών Εφαρμογών.
"\xa0\xa0\xa0\xa0Λεπτίνη, η ορμόνη ρυθμιστής της Ενέργειας" άρθρο που δημοσιεύτηκε στο\xa0terra papers"""
        ],
        
        "Παραμείνετε λεπτοί χωρίς δίαιτα": [
            "edw hellas",
            """\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0Ο θεράπων κλινικός διατροφολόγος λαμβάνοντας υπόψη τις πραγματικές ανάγκες του ασθενούς του και έχοντας υπόψη τα αντικειμενικά επιστημονικά δεδομένα για την κάθε θεραπεία που προτείνεται, μπορεί να συμβουλεύει στον ασθενή του εκείνο που είναι το πλέον κατάλληλο και ταυτόχρονα με τους λιγότερους κίνδυνους γι' αυτόν."""
        ]
    }
    
    for article in articles:
        title = article.get('title', '').strip()
        content = article.get('content', '')
        original_content = content
        
        # Check if this article has specific deletions
        if title in deletion_texts:
            print(f"Processing: {title}")
            
            for deletion_text in deletion_texts[title]:
                # Try exact match first
                if deletion_text in content:
                    content = content.replace(deletion_text, '')
                    changes_made.append({
                        'title': title,
                        'id': article.get('id'),
                        'source_file': article.get('source_file'),
                        'action': 'EXACT_DELETION',
                        'deleted_text': deletion_text[:100] + '...' if len(deletion_text) > 100 else deletion_text
                    })
                    print(f"  ✅ Deleted exact text")
                else:
                    # Try to find and delete with pattern matching for variations
                    # Handle non-breaking spaces and other variations
                    normalized_deletion = deletion_text.replace('\xa0', ' ').replace('\u200b', '').strip()
                    normalized_content = content.replace('\xa0', ' ').replace('\u200b', ' ')
                    
                    if normalized_deletion in normalized_content:
                        # Find the original text in content and delete it
                        # This is more complex, so we'll use regex for pattern matching
                        pattern = re.escape(normalized_deletion)
                        pattern = pattern.replace(r'\s+', r'\s*')  # Allow for whitespace variations
                        
                        # Create a more flexible pattern
                        flexible_pattern = re.sub(r'\\s\*', r'\\s*', pattern)
                        
                        new_content = re.sub(flexible_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
                        if new_content != content:
                            content = new_content
                            changes_made.append({
                                'title': title,
                                'id': article.get('id'),
                                'source_file': article.get('source_file'),
                                'action': 'PATTERN_DELETION',
                                'deleted_text': deletion_text[:100] + '...' if len(deletion_text) > 100 else deletion_text
                            })
                            print(f"  ✅ Deleted with pattern matching")
            
            # Clean up extra whitespace
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip()
            
            if content != original_content:
                article['content'] = content
    
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
    print("=== CORRECT PRECISE DELETIONS ===\n")
    
    # Load articles
    articles = load_articles()
    print(f"Total articles loaded: {len(articles)}\n")
    
    # Apply precise deletions
    modified_articles, changes_made = apply_correct_precise_deletions(articles)
    
    # Save changes
    save_articles(modified_articles)
    
    # Report
    print(f"\n=== CORRECT PRECISE DELETION REPORT ===")
    print(f"Total precise deletions: {len(changes_made)}")
    
    for change in changes_made:
        print(f"  - {change['title']} ({change['source_file']}) - {change['action']}")
    
    # Save report
    report = {
        'correct_precise_deletions': changes_made,
        'total_deletions': len(changes_made),
        'timestamp': '2025-02-27T07:15:00Z'
    }
    
    with open('correct_precise_deletions_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\nCorrect precise deletions report saved to correct_precise_deletions_report.json")

if __name__ == '__main__':
    main()

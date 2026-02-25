#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

with open('src/lib/content.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Check specific articles for their deletion texts
deletion_texts = {
    'Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!': 'Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!',
    'Η σεροτονίνη φέρνει ευτυχία κι επιτυχία': 'Κατερίνα Μηστριώτη       κλινική διατροφολόγος',
    'Το σωσίβιο είναι επικίνδυνο': 'TERRA PAPERS'
}

for post in data['posts']:
    title = post.get('title', 'Untitled')
    
    if title in deletion_texts:
        content = post.get('content', '')
        clean_content = re.sub(r'<[^>]*>', '', content)
        clean_content = re.sub(r'&nbsp;', ' ', clean_content)
        clean_content = re.sub(r'&amp;', '&', clean_content)
        clean_content = re.sub(r'\s+', ' ', clean_content)
        
        target_text = deletion_texts[title]
        
        print(f'=== {title} ===')
        print(f'Looking for: "{target_text}"')
        print(f'Found: {target_text in clean_content}')
        
        if target_text in clean_content:
            # Find context
            start = clean_content.find(target_text)
            context_start = max(0, start - 50)
            context_end = min(len(clean_content), start + len(target_text) + 50)
            print(f'Context: {repr(clean_content[context_start:context_end])}')
        print()

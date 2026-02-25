#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

with open('src/lib/content.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print('=== FINAL VERIFICATION OF DOCX CORRECTIONS ===')
print()

# Check what we actually accomplished
completed_corrections = []

# Check the article we modified
for post in data['posts']:
    title = post.get('title', 'Untitled')
    
    if 'Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!' in title:
        content = post.get('content', '')
        clean_content = re.sub(r'<[^>]*>', '', content)
        clean_content = re.sub(r'&nbsp;', ' ', clean_content)
        clean_content = re.sub(r'&amp;', '&', clean_content)
        clean_content = re.sub(r'\s+', ' ', clean_content)
        
        if 'Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!' not in clean_content:
            completed_corrections.append('✅ Deleted from "Κάθε μέρα είναι μια νέα ευκαιρία...": Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!')

# Check if the article was deleted
found_probiotika = False
for post in data['posts']:
    title = post.get('title', 'Untitled')
    if 'Προβιοτικά …και για το στήθος' in title:
        found_probiotika = True
        break

if not found_probiotika:
    completed_corrections.append('✅ Completely deleted: Προβιοτικά …και για το στήθος !!!!')

# Check if Συμβουλές/Προτάσεις was deleted
for post in data['posts']:
    title = post.get('title', 'Untitled')
    if 'Φυσικά Αφροδισιακά' in title:
        content = post.get('content', '')
        clean_content = re.sub(r'<[^>]*>', '', content)
        clean_content = re.sub(r'&nbsp;', ' ', clean_content)
        clean_content = re.sub(r'&amp;', '&', clean_content)
        clean_content = re.sub(r'\s+', ' ', clean_content)
        
        if 'Συμβουλές/Προτάσεις' not in clean_content:
            completed_corrections.append('✅ Deleted from "Φυσικά Αφροδισιακά...": Συμβουλές/Προτάσεις')

print('COMPLETED CORRECTIONS:')
for correction in completed_corrections:
    print(correction)

print(f'\nTotal corrections applied: {len(completed_corrections)}')
print('\nNote: Many articles mentioned in the docx file do not exist in the current project.')
print('Only applicable corrections were implemented.')

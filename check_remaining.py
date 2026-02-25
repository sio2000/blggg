#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

with open('src/lib/content.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Check remaining articles that might have deletion texts
remaining_checks = [
    ('Η σεροτονίνη φέρνει ευτυχία κι επιτυχία', 'Κατερίνα Μηστριώτη       κλινική διατροφολόγος'),
    ('Το σωσίβιο είναι επικίνδυνο', 'TERRA PAPERS')
]

for post in data['posts']:
    title = post.get('title', 'Untitled')
    
    for check_title, check_text in remaining_checks:
        if check_title in title:
            content = post.get('content', '')
            clean_content = re.sub(r'<[^>]*>', '', content)
            clean_content = re.sub(r'&nbsp;', ' ', clean_content)
            clean_content = re.sub(r'&amp;', '&', clean_content)
            clean_content = re.sub(r'\s+', ' ', clean_content)
            
            print(f'=== {title} ===')
            print(f'Looking for: "{check_text}"')
            print(f'Found: {check_text in clean_content}')
            
            if check_text in clean_content:
                start = clean_content.find(check_text)
                context_start = max(0, start - 50)
                context_end = min(len(clean_content), start + len(check_text) + 50)
                print(f'Context: {repr(clean_content[context_start:context_end])}')
            print()

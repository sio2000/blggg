#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('src/lib/content.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print('=== AVAILABLE ARTICLES ===')
for post in data['posts']:
    title = post.get('title', 'Untitled')
    print(f'- {title}')

print(f'Total articles: {len(data["posts"])}')

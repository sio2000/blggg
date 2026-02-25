#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os

def apply_corrections_fixed():
    """
    Apply corrections exactly as specified in the docx file
    Only for articles that actually exist in the current project
    """
    
    # Files to scan
    files_to_scan = [
        "src/lib/content.json",
        "posts.json",
        "pages.json"
    ]
    
    # Texts to delete from end of articles (only for existing articles)
    end_deletions = [
        {
            "article_title": "Κάθε μέρα είναι μια νέα ευκαιρία να χτίσουμε ένα νέο σώμα!  Ξεκινάμε ΣΗΜΕΡΑ !!!",
            "text_to_delete": "Μιλήστε μαζί μας και θα έχετε ακριβώς την βοήθεια που χρειάζεστε!!!"
        },
        {
            "article_title": "Φυσικά Αφροδισιακά για άνδρες και γυναίκες",
            "text_to_delete": "Συμβουλές/Προτάσεις"
        },
        {
            "article_title": "Η σεροτονίνη φέρνει ευτυχία κι επιτυχία",
            "text_to_delete": "Κατερίνα Μηστριώτη       κλινική διατροφολόγος"
        },
        {
            "article_title": "Το σωσίβιο είναι επικίνδυνο",
            "text_to_delete": "TERRA PAPERS"
        }
    ]
    
    # Articles to delete completely (only if they exist)
    complete_deletions = [
        "Προβιοτικά …και για το στήθος !!!!"
    ]
    
    total_deletions = 0
    deletion_report = {}
    
    print("=== APPLYING CORRECTIONS FROM DOCX FILE (FIXED) ===")
    print(f"Files to scan: {len(files_to_scan)}")
    print(f"End deletions: {len(end_deletions)}")
    print(f"Complete deletions: {len(complete_deletions)}")
    print()
    
    for file_path in files_to_scan:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        print(f"Processing {file_path}...")
        
        # Read the file (handle BOM)
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        # Parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {file_path}: {e}")
            continue
        
        # Handle different JSON structures
        posts = []
        if file_path == "src/lib/content.json":
            posts = data.get("posts", [])
        elif file_path in ["posts.json", "pages.json"]:
            if "feed" in data and "entry" in data["feed"]:
                posts = data["feed"]["entry"]
        
        file_deletions = 0
        file_report = {}
        posts_to_remove = []
        
        # Process each post/article
        for i, post in enumerate(posts):
            if not isinstance(post, dict):
                continue
                
            article_title = post.get("title", "Untitled")
            if isinstance(article_title, dict):
                article_title = article_title.get("$t", "Untitled")
            
            # Check if article should be completely deleted
            should_delete_completely = False
            for deletion_title in complete_deletions:
                if deletion_title in article_title:
                    should_delete_completely = True
                    break
            
            if should_delete_completely:
                posts_to_remove.append(i)
                file_deletions += 1
                total_deletions += 1
                if "Complete deletions" not in file_report:
                    file_report["Complete deletions"] = []
                file_report["Complete deletions"].append(article_title)
                continue
            
            # Check for end deletions
            if "content" not in post:
                continue
                
            original_content = post["content"]
            if isinstance(original_content, dict):
                original_content = original_content.get("$t", "")
            
            content_modified = False
            article_deletions = {}
            
            for deletion in end_deletions:
                target_title = deletion["article_title"]
                text_to_delete = deletion["text_to_delete"]
                
                # Check if this is the target article (partial match)
                if target_title in article_title or article_title in target_title:
                    # Clean content for comparison
                    clean_content = re.sub(r'<[^>]*>', '', original_content)
                    clean_content = re.sub(r'&nbsp;', ' ', clean_content)
                    clean_content = re.sub(r'&amp;', '&', clean_content)
                    clean_content = re.sub(r'\s+', ' ', clean_content)
                    
                    # Check if the text to delete exists
                    clean_delete_text = re.sub(r'\s+', ' ', text_to_delete)
                    
                    if clean_delete_text in clean_content:
                        # Find and delete in original content
                        new_content = original_content
                        
                        # Try direct replacement first
                        if text_to_delete in new_content:
                            new_content = new_content.replace(text_to_delete, "")
                        else:
                            # Try with cleaned version using regex
                            words = text_to_delete.split()
                            if len(words) > 1:
                                pattern_parts = []
                                for word in words:
                                    escaped_word = re.escape(word)
                                    pattern_parts.append(f'{escaped_word}\\s*(?:<[^>]*>\\s*)*')
                                pattern = ''.join(pattern_parts)
                                
                                matches = re.findall(pattern, new_content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                                if matches:
                                    new_content = re.sub(pattern, "", new_content, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
                        
                        if new_content != original_content:
                            post["content"] = new_content
                            content_modified = True
                            article_deletions[f"Deleted: {text_to_delete[:50]}..."] = 1
                            file_deletions += 1
                            total_deletions += 1
            
            # Record deletions for this article
            if content_modified:
                file_report[article_title] = article_deletions
        
        # Remove articles marked for complete deletion
        if posts_to_remove:
            # Remove in reverse order to maintain indices
            for i in reversed(posts_to_remove):
                if i < len(posts):
                    del posts[i]
        
        # Save modified file if changes were made
        if file_deletions > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✅ Updated {file_path} - {file_deletions} deletions")
                deletion_report[file_path] = file_report
            except Exception as e:
                print(f"Error saving {file_path}: {e}")
        else:
            print(f"✅ No deletions needed in {file_path}")
    
    # Generate final report
    print("\n" + "="*80)
    print("CORRECTIONS APPLIED REPORT")
    print("="*80)
    print(f"Total deletions performed: {total_deletions}")
    
    if total_deletions == 0:
        print("No matches were detected for any of the target texts.")
    else:
        print("\nDeletions by file:")
        for file_path, file_report in deletion_report.items():
            print(f"\n{file_path}:")
            for article_title, phrases_deleted in file_report.items():
                if article_title == "Complete deletions":
                    print(f"  Articles completely deleted:")
                    for deleted_title in phrases_deleted:
                        print(f"    - {deleted_title}")
                else:
                    print(f"  Article: {article_title}")
                    for phrase, count in phrases_deleted.items():
                        print(f"    - {phrase}: {count} deletion(s)")
    
    print("\n" + "="*80)
    print("CORRECTIONS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    apply_corrections_fixed()

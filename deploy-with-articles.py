#!/usr/bin/env python3
"""
Deployment script to ensure articles are synced to Netlify
This should be run before deploying to Netlify
"""

import json
import os
import subprocess
import sys

def check_articles_file():
    """Check if articles.json exists and has content"""
    try:
        with open('.data/articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"✓ Found {len(articles)} articles in .data/articles.json")
        return True, len(articles)
    except FileNotFoundError:
        print("✗ .data/articles.json not found")
        return False, 0
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing .data/articles.json: {e}")
        return False, 0

def run_build():
    """Run the Next.js build process"""
    print("\n=== Building Next.js Application ===")
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✓ Build successful")
            return True
        else:
            print("✗ Build failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("✗ Build timed out")
        return False
    except FileNotFoundError:
        print("✗ npm not found. Make sure Node.js is installed")
        return False

def deploy_to_netlify():
    """Deploy to Netlify using CLI"""
    print("\n=== Deploying to Netlify ===")
    try:
        # Check if Netlify CLI is installed
        result = subprocess.run(['netlify', '--version'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("✗ Netlify CLI not found. Install with: npm install -g netlify-cli")
            return False
        
        # Deploy to Netlify
        print("Deploying to Netlify...")
        result = subprocess.run(['netlify', 'deploy', '--prod', '--dir=.next'], 
                              capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✓ Deployment successful")
            print("Output:", result.stdout)
            return True
        else:
            print("✗ Deployment failed")
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Deployment timed out")
        return False

def main():
    print("=== Netlify Deployment with Articles ===\n")
    
    # Check articles
    has_articles, article_count = check_articles_file()
    if not has_articles:
        print("\n❌ No articles found. Please ensure .data/articles.json exists.")
        sys.exit(1)
    
    print(f"📄 Ready to deploy {article_count} articles")
    
    # Ask for confirmation
    confirm = input("\nProceed with build and deployment? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Deployment cancelled.")
        return
    
    # Build
    if not run_build():
        print("\n❌ Build failed. Fix errors before deploying.")
        sys.exit(1)
    
    # Deploy
    if deploy_to_netlify():
        print("\n🎉 Deployment complete!")
        print("Your articles should now be visible on Netlify.")
        print("\nImportant: The first load may take a minute as articles sync to Netlify Blobs.")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

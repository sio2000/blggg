#!/usr/bin/env python3
"""
Deploy to Netlify and sync all articles automatically
"""

import subprocess
import sys
import time
import requests

def run_command(cmd, description, timeout=300):
    """Run a command and handle errors"""
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print(f"✓ {description} successful")
            if result.stdout:
                print("Output:", result.stdout[:500])
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print("Error:", result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out")
        return False
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False

def deploy_to_netlify():
    """Deploy using Netlify CLI"""
    return run_command("netlify deploy --prod --dir=.next", "Deploying to Netlify", timeout=600)

def sync_after_deploy(netlify_url):
    """Sync articles after deployment"""
    print(f"\n=== SYNCING ARTICLES TO {netlify_url} ===")
    
    # Wait a bit for deployment to settle
    print("Waiting 30 seconds for deployment to settle...")
    time.sleep(30)
    
    try:
        response = requests.post(f"{netlify_url}/api/sync-articles", timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Sync successful: {result['message']}")
            print(f"  Articles synced: {result['localCount']}")
            return True
        else:
            print(f"✗ Sync failed: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Sync error: {e}")
        return False

def main():
    print("=== DEPLOY AND SYNC TO NETLIFY ===")
    print("This will build, deploy, and sync all your articles automatically\n")
    
    # Step 1: Build
    if not run_command("npm run build", "Building Next.js app"):
        print("\n❌ Build failed. Fix errors before deploying.")
        sys.exit(1)
    
    # Step 2: Deploy
    if not deploy_to_netlify():
        print("\n❌ Deployment failed. Check Netlify CLI setup.")
        sys.exit(1)
    
    # Step 3: Get the deployed URL and sync
    # For now, we'll use a placeholder - you should replace this with your actual URL
    netlify_url = "https://your-blog-name.netlify.app"  # UPDATE THIS
    
    print(f"\n=== DEPLOYMENT COMPLETE ===")
    print(f"Your site is deployed to: {netlify_url}")
    
    # Step 4: Sync articles
    if sync_after_deploy(netlify_url):
        print("\n🎉 ALL DONE!")
        print("✓ Site deployed")
        print("✓ Articles synced")
        print(f"✓ Visit {netlify_url} to see all your articles")
    else:
        print("\n⚠️  Deployment succeeded but sync failed.")
        print("Run 'python force-sync.py' manually to sync articles.")

if __name__ == '__main__':
    main()

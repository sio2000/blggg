#!/usr/bin/env node

/**
 * Script to sync local articles to Netlify Blobs
 * This script will upload all articles from .data/articles.json to Netlify production storage
 */

const fs = require('fs').promises;
const path = require('path');
const { getStore } = require('@netlify/blobs');

async function loadLocalArticles() {
  try {
    const dataPath = path.join(process.cwd(), '.data', 'articles.json');
    const data = await fs.readFile(dataPath, 'utf-8');
    const articles = JSON.parse(data);
    console.log(`✓ Loaded ${articles.length} articles from .data/articles.json`);
    return articles;
  } catch (error) {
    console.error('✗ Error loading local articles:', error.message);
    return [];
  }
}

async function syncToNetlifyBlobs(articles) {
  try {
    console.log('\n=== Syncing to Netlify Blobs ===');
    
    // Set Netlify environment variables for the script
    // You'll need to set these environment variables before running:
    // NETLIFY_SITE_ID=your-site-id
    // NETLIFY_AUTH_TOKEN=your-auth-token
    
    if (!process.env.NETLIFY_SITE_ID) {
      console.error('✗ NETLIFY_SITE_ID environment variable is required');
      console.log('Please run: export NETLIFY_SITE_ID=your-site-id');
      return false;
    }
    
    const store = getStore({
      name: 'articles',
      siteID: process.env.NETLIFY_SITE_ID,
      token: process.env.NETLIFY_AUTH_TOKEN
    });
    
    // Upload all articles to Netlify Blobs
    await store.setJSON('all-articles', articles);
    console.log(`✓ Successfully uploaded ${articles.length} articles to Netlify Blobs`);
    
    // Verify the upload
    const verifyData = await store.get('all-articles', { type: 'json' });
    if (verifyData && verifyData.length === articles.length) {
      console.log('✓ Verification successful: All articles are stored in Netlify Blobs');
      return true;
    } else {
      console.log('⚠️  Verification warning: Article count mismatch');
      return false;
    }
    
  } catch (error) {
    console.error('✗ Error syncing to Netlify Blobs:', error.message);
    console.error('Full error:', error);
    return false;
  }
}

async function createBackupScript() {
  // Create a simpler backup approach using the API
  const backupScript = `
#!/usr/bin/env node

/**
 * Backup script to upload articles via API endpoint
 * Run this on your deployed Netlify site
 */

const fs = require('fs').promises;
const path = require('path');

async function uploadViaAPI() {
  try {
    // Load local articles
    const dataPath = path.join(process.cwd(), '.data', 'articles.json');
    const data = await fs.readFile(dataPath, 'utf-8');
    const articles = JSON.parse(data);
    
    console.log(\`Loaded \${articles.length} articles\`);
    
    // Upload each article via API
    let successCount = 0;
    const siteUrl = process.env.NETLIFY_URL || 'https://your-site-name.netlify.app';
    
    for (const article of articles) {
      try {
        const response = await fetch(\`\${siteUrl}/api/articles\`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: article.title,
            content: article.content,
            imageUrl: article.imageUrl,
            author: article.author,
            labels: article.labels || [],
            category: article.category || 'Αρχική σελίδα'
          })
        });
        
        if (response.ok) {
          successCount++;
          console.log(\`✓ Uploaded: \${article.title.substring(0, 50)}...\`);
        } else {
          console.log(\`✗ Failed: \${article.title.substring(0, 50)}... - \${response.status}\`);
        }
        
        // Small delay
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        console.log(\`✗ Error: \${article.title.substring(0, 50)}... - \${error.message}\`);
      }
    }
    
    console.log(\`\\nComplete: \${successCount}/\${articles.length} articles uploaded\`);
  } catch (error) {
    console.error('Error:', error);
  }
}

uploadViaAPI();
`;

  await fs.writeFile('upload-via-api.js', backupScript);
  console.log('✓ Created upload-via-api.js backup script');
}

async function main() {
  console.log('=== Article Sync Tool ===\n');
  
  // Load local articles
  const articles = await loadLocalArticles();
  if (!articles.length) {
    console.log('No articles to sync. Exiting.');
    return;
  }
  
  console.log(`Found ${articles.length} articles to sync\n`);
  
  // Try direct Netlify Blobs sync first
  const blobsSuccess = await syncToNetlifyBlobs(articles);
  
  if (!blobsSuccess) {
    console.log('\n=== Alternative Method ===');
    console.log('Direct Netlify Blobs sync failed. Creating backup script...');
    await createBackupScript();
    
    console.log('\n=== Manual Instructions ===');
    console.log('1. Set your Netlify credentials:');
    console.log('   export NETLIFY_SITE_ID=your-site-id');
    console.log('   export NETLIFY_AUTH_TOKEN=your-auth-token');
    console.log('2. Run this script again');
    console.log('3. Or use the upload-via-api.js script on your deployed site');
  }
}

main().catch(console.error);

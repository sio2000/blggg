/**
 * Article synchronization utility
 * This ensures articles are available both locally and on Netlify
 */

import { getArticles, saveArticles } from './db';
import fs from 'fs/promises';
import path from 'path';

// Local file paths
const dataDir = path.join(process.cwd(), '.data');
const articlesFile = path.join(dataDir, 'articles.json');

// Load articles from local file
async function loadLocalArticles(): Promise<any[]> {
  try {
    const data = await fs.readFile(articlesFile, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.log('No local articles file found, starting fresh');
    return [];
  }
}

// Save articles to local file
async function saveLocalArticles(articles: any[]): Promise<void> {
  try {
    await fs.mkdir(dataDir, { recursive: true });
    await fs.writeFile(articlesFile, JSON.stringify(articles, null, 2), 'utf-8');
  } catch (error) {
    console.error('Error saving local articles:', error);
  }
}

// Main sync function - ensures both local and Netlify storage have the same articles
export async function syncArticles(): Promise<void> {
  try {
    console.log('Starting article synchronization...');
    
    // Load from both sources
    const localArticles = await loadLocalArticles();
    const netlifyArticles = await getArticles();
    
    console.log(`Local articles: ${localArticles.length}`);
    console.log(`Netlify articles: ${netlifyArticles.length}`);
    
    // If local has more articles, sync to Netlify
    if (localArticles.length > netlifyArticles.length) {
      console.log('Syncing local articles to Netlify...');
      await saveArticles(localArticles);
      console.log(`Synced ${localArticles.length} articles to Netlify`);
    }
    // If Netlify has more articles, sync to local
    else if (netlifyArticles.length > localArticles.length) {
      console.log('Syncing Netlify articles to local...');
      await saveLocalArticles(netlifyArticles);
      console.log(`Synced ${netlifyArticles.length} articles to local`);
    }
    // If counts are same, ensure they're actually the same
    else {
      // For simplicity, we'll use Netlify as the source of truth
      await saveLocalArticles(netlifyArticles);
      console.log('Articles are already in sync');
    }
    
  } catch (error) {
    console.error('Error during sync:', error);
  }
}

// Initialize sync on application start
export async function initializeArticleSync(): Promise<void> {
  // Only run sync in production or when explicitly requested
  const isProduction = process.env.NODE_ENV === 'production';
  const shouldSync = isProduction || process.env.FORCE_SYNC === 'true';
  
  if (shouldSync) {
    await syncArticles();
  }
}

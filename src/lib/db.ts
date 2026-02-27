import fs from "fs/promises";
import path from "path";
import { getStore } from "@netlify/blobs";

// Article interface matching the existing Post structure
export interface Article {
  id: string;
  title: string;
  content: string;
  imageUrl: string | null;
  published: string;
  author: string;
  labels: string[];
  category: string; // New: category/tab name (Articles, Healthy Life Style, etc.)
  createdAt: string;
}

// Store name for articles
const ARTICLES_STORE = "articles";
const ARTICLES_KEY = "all-articles";
const IMAGES_STORE = "images";

// Check if running on Netlify (production)
// Use multiple checks for reliability
const isNetlify = 
  process.env.NETLIFY === "true" || 
  process.env.CONTEXT !== undefined ||
  process.env.DEPLOY_ID !== undefined ||
  process.env.SITE_ID !== undefined ||
  process.env.NETLIFY_BUILD_BASE !== undefined;

// Local JSON file storage
const dataDir = path.join(process.cwd(), ".data");
const articlesFile = path.join(dataDir, "articles.json");
const imagesDir = path.join(dataDir, "images");

// Ensure data directory exists
async function ensureDataDirs() {
  try {
    await fs.mkdir(dataDir, { recursive: true });
    await fs.mkdir(imagesDir, { recursive: true });
  } catch (error) {
    console.error("Error creating data directories:", error);
  }
}

// Get all articles
export async function getArticles(): Promise<Article[]> {
  try {
    const inNetlifyFunctionsTemp = process.cwd().includes("/var/task/");
    
    if (!isNetlify && !inNetlifyFunctionsTemp) {
      // Local development: use JSON file storage
      await ensureDataDirs();
      try {
        const data = await fs.readFile(articlesFile, "utf-8");
        return JSON.parse(data);
      } catch (error) {
        // File doesn't exist yet, return empty array
        return [];
      }
    }

    // Production on Netlify - always use Blobs
    const store = getStore(ARTICLES_STORE);
    const data = await store.get(ARTICLES_KEY, { type: "json" });
    
    // ALWAYS try to sync from local file to ensure we have all articles
    if (!inNetlifyFunctionsTemp) {
      try {
        const localData = await fs.readFile(articlesFile, "utf-8");
        const localArticles = JSON.parse(localData);
        
        if (localArticles.length > 0) {
          console.log(`Found ${localArticles.length} local articles, ensuring they're on Netlify...`);
          
          // Always upload local articles to ensure they're available
          await store.setJSON(ARTICLES_KEY, localArticles);
          console.log("Successfully synced local articles to Netlify");
          return localArticles;
        }
      } catch (localError) {
        console.log("Could not load local articles:", localError);
      }
    }
    
    return (data as Article[]) || [];
  } catch (error) {
    console.error("Error fetching articles:", error);
    return [];
  }
}

// Get single article by ID
export async function getArticleById(id: string): Promise<Article | null> {
  const articles = await getArticles();
  return articles.find((a) => a.id === id) || null;
}

// Save all articles
export async function saveArticles(articles: Article[]): Promise<void> {
  try {
    const inNetlifyFunctionsTemp = process.cwd().includes("/var/task/");
    
    if (!isNetlify && !inNetlifyFunctionsTemp) {
      // Local development: save to JSON file
      await ensureDataDirs();
      await fs.writeFile(articlesFile, JSON.stringify(articles, null, 2), "utf-8");
      return;
    }

    // Production on Netlify - always use Blobs
    const store = getStore(ARTICLES_STORE);
    await store.setJSON(ARTICLES_KEY, articles);
  } catch (error) {
    console.error("Error saving articles:", error);
    throw error;
  }
}

// Create a new article
export async function createArticle(
  article: Omit<Article, "id" | "createdAt" | "published">
): Promise<Article> {
  const articles = await getArticles();

  const newArticle: Article = {
    ...article,
    id: `article-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    published: new Date().toISOString(),
    createdAt: new Date().toISOString(),
  };

  articles.unshift(newArticle); // Add to beginning (newest first)
  await saveArticles(articles);

  return newArticle;
}

// Update an article
export async function updateArticle(
  id: string,
  updates: Partial<Omit<Article, "id" | "createdAt">>
): Promise<Article | null> {
  const articles = await getArticles();
  const index = articles.findIndex((a) => a.id === id);

  if (index === -1) return null;

  articles[index] = { ...articles[index], ...updates };
  await saveArticles(articles);

  return articles[index];
}

// Delete an article
export async function deleteArticle(id: string): Promise<boolean> {
  const articles = await getArticles();
  const index = articles.findIndex((a) => a.id === id);

  if (index === -1) return false;

  articles.splice(index, 1);
  await saveArticles(articles);

  return true;
}

// Upload an image and return the URL
export async function uploadImage(
  filename: string,
  data: string, // base64 encoded
  contentType: string
): Promise<string> {
  const imageId = `img-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const extension = filename.split(".").pop() || "jpg";
  const key = `${imageId}.${extension}`;

  try {
    // IMPORTANT: /var/task/ is Netlify Functions temp directory - never use for persistence
    const inNetlifyFunctionsTemp = process.cwd().includes("/var/task/");
    
    if (!isNetlify && !inNetlifyFunctionsTemp) {
      // Local development: save to file
      await ensureDataDirs();
      const buffer = Buffer.from(data, "base64");
      await fs.writeFile(path.join(imagesDir, key), buffer);
      return `/api/images/${key}`;
    }

    // Production on Netlify - always use Blobs
    try {
      const store = getStore(IMAGES_STORE);
      const buffer = Buffer.from(data, "base64");
      const arrayBuffer = buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);
      await store.set(key, arrayBuffer, { metadata: { contentType } });
      return `/api/images/${key}`;
    } catch (storeError) {
      const storeErrorMsg = storeError instanceof Error ? storeError.message : String(storeError);
      console.error("Netlify Blobs store error:", storeErrorMsg);
      console.error("Store error details:", storeError);
      throw new Error(`Netlify Blobs store failed: ${storeErrorMsg}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    console.error("Error uploading image:", errorMessage);
    console.error("Full error:", error);
    console.error("isNetlify:", isNetlify);
    console.error("cwd:", process.cwd());
    throw new Error(`Image upload failed: ${errorMessage}`);
  }
}

// Get an image
export async function getImage(
  key: string
): Promise<{ data: Buffer; contentType: string } | null> {
  try {
    const inNetlifyFunctionsTemp = process.cwd().includes("/var/task/");
    
    if (!isNetlify && !inNetlifyFunctionsTemp) {
      // Local development: read from file
      await ensureDataDirs();
      try {
        const data = await fs.readFile(path.join(imagesDir, key));
        return {
          data,
          contentType: key.endsWith(".png")
            ? "image/png"
            : key.endsWith(".gif")
            ? "image/gif"
            : key.endsWith(".webp")
            ? "image/webp"
            : "image/jpeg",
        };
      } catch {
        return null;
      }
    }

    // Production on Netlify - always use Blobs
    const store = getStore(IMAGES_STORE);
    const blob = await store.get(key, { type: "arrayBuffer" });
    if (!blob) return null;

    const metadata = await store.getMetadata(key);
    const contentType =
      (metadata?.metadata as { contentType?: string })?.contentType ||
      "image/jpeg";

    return {
      data: Buffer.from(blob),
      contentType,
    };
  } catch (error) {
    console.error("Error getting image:", error);
    return null;
  }
}

import { NextResponse } from "next/server";
import { getArticles, saveArticles } from "@/lib/db";
import fs from "fs/promises";
import path from "path";

// Force sync all articles from local file to Netlify
export async function POST() {
  try {
    console.log("=== FORCE SYNCING ARTICLES TO NETLIFY ===");
    
    // Load local articles
    const dataDir = path.join(process.cwd(), ".data");
    const articlesFile = path.join(dataDir, "articles.json");
    
    try {
      const localData = await fs.readFile(articlesFile, "utf-8");
      const localArticles = JSON.parse(localData);
      
      console.log(`Loaded ${localArticles.length} articles from local file`);
      
      // Save to Netlify (this will use Netlify Blobs in production)
      await saveArticles(localArticles);
      
      // Verify by getting them back
      const verifyArticles = await getArticles();
      
      console.log(`Verification: ${verifyArticles.length} articles on Netlify`);
      
      return NextResponse.json({
        success: true,
        message: `Successfully synced ${localArticles.length} articles to Netlify`,
        localCount: localArticles.length,
        netlifyCount: verifyArticles.length
      });
      
    } catch (fileError) {
      console.error("Error reading local articles file:", fileError);
      return NextResponse.json(
        { error: "Could not read local articles file" },
        { status: 500 }
      );
    }
    
  } catch (error) {
    console.error("Error during sync:", error);
    return NextResponse.json(
      { error: "Failed to sync articles" },
      { status: 500 }
    );
  }
}

// GET endpoint to check sync status
export async function GET() {
  try {
    const articles = await getArticles();
    
    // Try to get local count
    let localCount = 0;
    try {
      const dataDir = path.join(process.cwd(), ".data");
      const articlesFile = path.join(dataDir, "articles.json");
      const localData = await fs.readFile(articlesFile, "utf-8");
      const localArticles = JSON.parse(localData);
      localCount = localArticles.length;
    } catch {
      // Local file doesn't exist or can't be read
    }
    
    return NextResponse.json({
      netlifyCount: articles.length,
      localCount: localCount,
      inSync: articles.length === localCount && localCount > 0
    });
    
  } catch (error) {
    console.error("Error checking sync status:", error);
    return NextResponse.json(
      { error: "Failed to check sync status" },
      { status: 500 }
    );
  }
}

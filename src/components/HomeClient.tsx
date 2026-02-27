"use client";

import React, { useEffect, useState } from "react";
import PostList from "./sections/post-list";
import content from "@/lib/content.json";

interface Article {
  id: string;
  title: string;
  content: string;
  imageUrl: string | null;
  published: string;
  author: string;
  labels: string[];
  category: string;
  createdAt: string;
}

function articleToPost(article: Article) {
  let contentWithImage = article.content;
  if (article.imageUrl && !article.content.includes("<img")) {
    contentWithImage = `<img src="${article.imageUrl}" alt="${article.title}" />${article.content}`;
  }

  return {
    id: article.id,
    published: article.published,
    title: article.title,
    content: contentWithImage,
    author: article.author,
    labels: article.labels || [],
  };
}

// Remove duplicate articles based on title
function removeDuplicatesByTitle(posts: any[]) {
  const seen = new Set();
  return posts.filter(post => {
    const normalizedTitle = post.title?.trim().toLowerCase();
    if (!normalizedTitle) return false;
    
    if (seen.has(normalizedTitle)) {
      console.log(`Removing duplicate: ${post.title}`);
      return false;
    }
    
    seen.add(normalizedTitle);
    return true;
  });
}

// Sort posts - put specific article first, then by date
function sortPosts(posts: any[]) {
  // Find the target article by multiple criteria
  let targetIndex = posts.findIndex(p => 
    p.title?.toLowerCase().includes("μήπως δεν εκτίδεστε όσο πρέπει") || 
    p.title?.toLowerCase().includes("εκτεθείτε στον ήλιο")
  );
  
  // If not found by title, try by content
  if (targetIndex === -1) {
    targetIndex = posts.findIndex(p => 
      p.content?.toLowerCase().includes("εκτεθείτε") && 
      p.content?.toLowerCase().includes("ήλιο") &&
      p.content?.toLowerCase().includes("βιταμίνης") &&
      p.content?.toLowerCase().includes("καρκίνου")
    );
  }
  
  if (targetIndex !== -1) {
    // Move target article to the beginning
    const targetPost = posts[targetIndex];
    posts.splice(targetIndex, 1);
    posts.unshift(targetPost);
    console.log("Target article found and moved to position 0");
    console.log("Target title:", targetPost.title);
  } else {
    console.log("Target article NOT found!");
    console.log("Available titles:");
    posts.forEach((p, i) => console.log(`${i}: ${p.title}`));
  }
  
  return posts;
}

export default function HomeClient() {
  const [dbPosts, setDbPosts] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function fetchArticles() {
      try {
        const res = await fetch("/api/articles");
        if (!res.ok) throw new Error(`Articles fetch failed: ${res.status}`);
        const data = await res.json();
        if (mounted && data.articles) setDbPosts(data.articles);
      } catch (err) {
        console.error("Error fetching articles:", err);
      } finally {
        if (mounted) setIsLoading(false);
      }
    }

    fetchArticles();
    return () => { mounted = false };
  }, []);

  // Show ALL legacy articles from content.json
  const legacyPosts = Array.isArray(content.posts)
    ? content.posts
    : [];

  // Show ALL articles from database (no category filter)
  const allDbArticles = dbPosts;

  const allPosts = [
    ...allDbArticles.map(articleToPost),
    ...legacyPosts,
  ];

  // Remove duplicates based on title
  const uniquePosts = removeDuplicatesByTitle(allPosts);
  
  // Sort posts - put target article first
  const sortedPosts = sortPosts(uniquePosts);
  
  console.log(`Total posts before deduplication: ${allPosts.length}`);
  console.log(`Unique posts after deduplication: ${uniquePosts.length}`);
  
  // Debug: Print all titles to find the target article
  console.log("All article titles:");
  sortedPosts.forEach((post, index) => {
    console.log(`${index}: ${post.title}`);
  });
  
  console.log(`Target article position: ${sortedPosts.findIndex(p => 
    p.title?.toLowerCase().includes("μήπως δεν εκτίδεστε όσο πρέπει") || 
    p.title?.toLowerCase().includes("εκτεθείτε στον ήλιο")
  )}`);

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-gray-100">
        <div className="w-8 h-8 border-4 border-t-transparent rounded-full animate-spin mx-auto" style={{ borderColor: 'rgba(12, 6, 247, 0.2)', borderTopColor: '#0c06f7' }}></div>
        <p className="mt-4 text-gray-500">Φόρτωση άρθρων...</p>
      </div>
    );
  }

  return <PostList posts={sortedPosts} />;
}

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

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center shadow-sm border border-gray-100">
        <div className="w-8 h-8 border-4 border-t-transparent rounded-full animate-spin mx-auto" style={{ borderColor: 'rgba(12, 6, 247, 0.2)', borderTopColor: '#0c06f7' }}></div>
        <p className="mt-4 text-gray-500">Φόρτωση άρθρων...</p>
      </div>
    );
  }

  return <PostList posts={allPosts} />;
}

"use client";

import React from "react";
import Header from "@/components/sections/header";
import Sidebar from "@/components/sections/sidebar";
import Credits from "@/components/sections/credits";
import CategoryClient from "@/components/CategoryClient";
import { motion } from "framer-motion";
import { ArrowLeft, Tag } from "lucide-react";
import Link from "next/link";

const categoryNames: { [key: string]: string } = {
  articles: "Articles",
  "healthy-life-style": "Healthy Life Style",
  "syntagés-dýnamis": "Συνταγές Δύναμης",
  "sensitiv-imago": "Sensitiv Imago",
};

export default function CategoryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = React.use(params);
  // Decode the slug to get the proper display name
  const decodedSlug = decodeURIComponent(slug);
  const categoryDisplayName = categoryNames[decodedSlug] || decodedSlug;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />

      {/* Category Header */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-gray-500 transition-colors mb-4 hover:opacity-70"
            style={{ color: '#0c06f7' }}
          >
            <ArrowLeft className="w-4 h-4" />
            Πίσω στην αρχική
          </Link>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-4"
          >
            <div className="w-14 h-14 rounded-2xl flex items-center justify-center" style={{ backgroundColor: 'rgba(12, 6, 247, 0.05)' }}>
              <Tag className="w-7 h-7" style={{ color: '#0c06f7' }} />
            </div>
            <div>
              <p className="text-sm text-gray-500 mb-1">Κατηγορία</p>
              <h1 className="text-2xl md:text-3xl font-semibold text-gray-900" style={{ fontFamily: 'Constantia, serif', color: '#0c06f7' }}>
                {categoryDisplayName}
              </h1>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-10">
          {/* Main Content */}
          <div className="flex-1 min-w-0">
            <CategoryClient category={categoryDisplayName} />
          </div>

          {/* Sidebar */}
          <div className="lg:sticky lg:top-24 lg:self-start">
            <Sidebar />
          </div>
        </div>
      </main>

      <Credits />
    </div>
  );
}

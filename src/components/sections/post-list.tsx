"use client";
import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { User, Tag, ArrowRight, Share2, Twitter, Facebook } from 'lucide-react';

interface Post {
  id: string;
  published: string;
  title: string;
  content: string;
  author: string;
  labels: string[];
}

interface PostListProps {
  posts: Post[];
}

const PostItem = ({ post, index }: { post: Post; index: number }) => {
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const date = new Date(post.published);
  const formattedDate = mounted ? date.toLocaleDateString('el-GR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }) : '';

  const formattedTime = mounted ? date.toLocaleTimeString('el-GR', {
    hour: 'numeric',
    minute: '2-digit'
  }) : '';

  // Generate correct post URL based on ID format
  const getPostUrl = (postId: string) => {
    // Handle different ID formats
    if (postId.startsWith('article-')) {
      // Database article format: article-timestamp-random
      return `/post/${postId}`;
    } else if (postId.includes('tag:blogger.com')) {
      // Legacy blogger format: tag:blogger.com,1999:blog-...post-...
      // Extract the post ID part after the last hyphen
      const parts = postId.split('-');
      return `/post/${parts[parts.length - 1]}`;
    } else {
      // Fallback
      return `/post/${postId}`;
    }
  };
  const imgMatch = post.content.match(/<img.*?src="(.*?)"/);
  const thumbnailSrc = imgMatch ? imgMatch[1] : null;

  // Extract clean text excerpt - decode HTML entities properly
  const decodeHtmlEntities = (text: string) => {
    let decoded = text;
    
    // First pass: decode double-encoded entities (e.g., &amp;nbsp; -> &nbsp;)
    decoded = decoded.replace(/&amp;/gi, '&');
    
    // Second pass: decode all HTML entities
    const entities: { [key: string]: string } = {
      '&nbsp;': ' ',
      '&amp;': '&',
      '&lt;': '<',
      '&gt;': '>',
      '&quot;': '"',
      '&#39;': "'",
      '&apos;': "'",
      '&ndash;': '–',
      '&mdash;': '—',
      '&hellip;': '…',
      '&laquo;': '«',
      '&raquo;': '»',
      '&copy;': '©',
      '&reg;': '®',
      '&trade;': '™',
      '&euro;': '€',
      '&pound;': '£',
      '&yen;': '¥',
      '&cent;': '¢',
      '&deg;': '°',
      '&plusmn;': '±',
      '&times;': '×',
      '&divide;': '÷',
      '&frac12;': '½',
      '&frac14;': '¼',
      '&frac34;': '¾',
    };
    
    Object.keys(entities).forEach(entity => {
      decoded = decoded.replace(new RegExp(entity, 'gi'), entities[entity]);
    });
    
    // Handle numeric HTML entities (e.g., &#160; for nbsp)
    decoded = decoded.replace(/&#(\d+);/g, (match, num) => {
      return String.fromCharCode(parseInt(num, 10));
    });
    
    // Handle hex HTML entities (e.g., &#x00A0;)
    decoded = decoded.replace(/&#x([0-9a-f]+);/gi, (match, hex) => {
      return String.fromCharCode(parseInt(hex, 16));
    });
    
    // Clean up multiple spaces
    decoded = decoded.replace(/\s+/g, ' ').trim();
    return decoded;
  };
  
  const textContent = post.content.replace(/<[^>]*>/g, '');
  const cleanText = decodeHtmlEntities(textContent);
  const excerpt = cleanText.substring(0, 200).trim() + '...';

  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        duration: 0.5, 
        delay: index * 0.1,
        ease: [0.25, 0.1, 0.25, 1]
      }}
      className="group"
    >
      <div className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-500 border border-stone-100 card-lift">
        {/* Card Image */}
        {thumbnailSrc && (
          <Link 
            href={getPostUrl(post.id)}
            className="block relative overflow-hidden aspect-[16/9] image-hover-zoom"
          >
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105"
              style={{ backgroundImage: `url(${thumbnailSrc})` }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </Link>
        )}
        
        {/* Card Content */}
        <div className="p-6 md:p-8">
          {/* Meta Info */}
          <div className="flex flex-wrap items-center gap-4 mb-4 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4" />
              <span>{post.author}</span>
            </div>
          </div>

          {/* Title */}
          <h2 className="mb-4">
            <Link 
              href={getPostUrl(post.id)}
              className="text-2xl md:text-3xl font-semibold text-gray-900 transition-colors duration-300 leading-tight link-hover-underline hover:opacity-70"
              style={{ fontFamily: 'Constantia, serif', color: '#0c06f7' }}
            >
              {post.title}
            </Link>
          </h2>

          {/* Excerpt */}
          <p className="text-gray-600 leading-relaxed mb-6 font-serif text-lg">
            {excerpt}
          </p>

          {/* Labels/Tags */}
          <div className="flex flex-wrap gap-2 mb-6">
            {post.labels.map((label) => (
              <Link
                key={label}
                href={`/search/label/${label}`}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-full transition-colors"
                style={{ backgroundColor: 'rgba(12, 6, 247, 0.1)', color: '#0c06f7' }}
              >
                <Tag className="w-3 h-3" />
                {label}
              </Link>
            ))}
          </div>

          {/* Footer Actions */}
          <div className="flex items-center justify-between pt-6 border-t border-stone-100">
            {/* Social Share */}
            <div className="flex items-center gap-2">
              <span className="text-xs text-gray-400 mr-2">Share:</span>
              <motion.button 
                onClick={() => window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.origin + getPostUrl(post.id))}&text=${encodeURIComponent(post.title)}`, '_blank')}
                className="w-9 h-9 flex items-center justify-center text-gray-400 hover:text-[#1DA1F2] hover:bg-blue-50 rounded-full transition-all"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                aria-label="Μοιραστείτε στο Twitter"
              >
                <Twitter className="w-4 h-4" />
              </motion.button>
              <motion.button 
                onClick={() => window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.origin + getPostUrl(post.id))}`, '_blank')}
                className="w-9 h-9 flex items-center justify-center text-gray-400 hover:text-[#4267B2] hover:bg-blue-50 rounded-full transition-all"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                aria-label="Μοιραστείτε στο Facebook"
              >
                <Facebook className="w-4 h-4" />
              </motion.button>
            </div>

            {/* Read More */}
            <Link 
              href={getPostUrl(post.id)}
              className="group/btn inline-flex items-center gap-2 px-6 py-2.5 text-sm font-bold rounded-full transition-all duration-300 shadow-sm hover:shadow-md btn-press"
              style={{ 
                backgroundColor: 'white',
                color: '#0c06f7',
                border: '2px solid #0c06f7'
              }}
            >
              Διαβάστε περισσότερα
              <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Posted Time */}
          <p className="mt-4 text-xs text-gray-400 italic">
            Αναρτήθηκε από <span className="text-gray-500">{post.author}</span> στις {formattedTime}
          </p>
        </div>
      </div>
    </motion.article>
  );
};

const PostList = ({ posts }: PostListProps) => {
  return (
    <div className="space-y-8">
      {posts.map((post, index) => (
        <PostItem key={post.id} post={post} index={index} />
      ))}
      
      {posts.length === 0 && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-2xl p-12 text-center shadow-sm border border-gray-100"
        >
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Tag className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-xl font-display font-semibold text-gray-700 mb-2">
            Δεν βρέθηκαν αναρτήσεις
          </h3>
          <p className="text-gray-500">
            Δεν υπάρχουν διαθέσιμες αναρτήσεις αυτή τη στιγμή.
          </p>
        </motion.div>
      )}
    </div>
  );
};

export default PostList;

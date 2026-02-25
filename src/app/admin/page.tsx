"use client";

import { useState, useEffect, useCallback } from "react";
import { useDropzone } from "react-dropzone";

// Hardcoded credentials - DO NOT CHANGE
const ADMIN_EMAIL = "nektar-t@otenet.gr";
const ADMIN_PASSWORD = "admin123456";

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

export default function AdminPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");

  // Article state
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Form state
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [labels, setLabels] = useState("");
  const [category, setCategory] = useState("Αρχική σελίδα"); // New: category selector
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Category options
  const categories = [
    "Αρχική σελίδα",
    "Articles",
    "Healthy Life Style",
    "Συνταγές Δύναμης",
    "Sensitiv Imago",
  ];

  // Edit mode
  const [editingArticle, setEditingArticle] = useState<Article | null>(null);

  // Check session on mount
  useEffect(() => {
    const session = sessionStorage.getItem("admin_authenticated");
    if (session === "true") {
      setIsAuthenticated(true);
    }
  }, []);

  // Fetch articles when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchArticles();
    }
  }, [isAuthenticated]);

  const fetchArticles = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/articles");
      const data = await response.json();
      if (data.articles) {
        setArticles(data.articles);
      }
    } catch (err) {
      setError("Failed to fetch articles");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");

    if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
      setIsAuthenticated(true);
      sessionStorage.setItem("admin_authenticated", "true");
    } else {
      setLoginError("Invalid email or password");
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    sessionStorage.removeItem("admin_authenticated");
    setEmail("");
    setPassword("");
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setImageFile(file);
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"],
      "image/gif": [".gif"],
      "image/webp": [".webp"],
    },
    maxFiles: 1,
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  const clearForm = () => {
    setTitle("");
    setContent("");
    setLabels("");
    setCategory("Αρχική σελίδα");
    setImageFile(null);
    setImagePreview(null);
    setEditingArticle(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsSubmitting(true);

    try {
      let imageUrl: string | null = editingArticle?.imageUrl || null;

      // Upload image if provided
      if (imageFile) {
        const formData = new FormData();
        formData.append("file", imageFile);

        const uploadResponse = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (!uploadResponse.ok) {
          const uploadError = await uploadResponse.json();
          throw new Error(uploadError.error || "Failed to upload image");
        }

        const uploadData = await uploadResponse.json();
        imageUrl = uploadData.imageUrl;
      }

      // Parse labels
      const labelArray = labels
        .split(",")
        .map((l) => l.trim())
        .filter((l) => l.length > 0);

      const articleData = {
        title,
        content,
        imageUrl,
        labels: labelArray,
        category,
        author: "Katerina Mistrioti",
      };

      let response;
      if (editingArticle) {
        // Update existing article
        response = await fetch("/api/articles", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: editingArticle.id, ...articleData }),
        });
      } else {
        // Create new article
        response = await fetch("/api/articles", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(articleData),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to save article");
      }

      setSuccess(
        editingArticle
          ? "Article updated successfully!"
          : "Article published successfully!"
      );
      clearForm();
      fetchArticles();
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = (article: Article) => {
    setEditingArticle(article);
    setTitle(article.title);
    setContent(article.content);
    setLabels(article.labels.join(", "));
    setCategory(article.category);
    setImageFile(null); // Clear file input
    if (article.imageUrl) {
      setImagePreview(article.imageUrl);
    } else {
      setImagePreview(null);
    }
    // Scroll to top of form
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this article?")) return;

    try {
      const response = await fetch(`/api/articles?id=${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete article");
      }

      setSuccess("Article deleted successfully!");
      fetchArticles();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete article");
    }
  };

  // Login form
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
          <h1 className="text-2xl font-bold text-gray-900 text-center mb-6">
            Σύνδεση Admin
          </h1>

          {loginError && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
              {loginError}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Κωδικός
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 transition-colors font-medium"
            >
              Σύνδεση
            </button>
          </form>
        </div>
      </div>
    );
  }

  // Admin panel
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Πίνακας Ελέγχου</h1>
          <button
            onClick={handleLogout}
            className="text-gray-600 hover:text-gray-900 text-sm"
          >
            Αποσύνδεση
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Alerts */}
        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-50 text-green-600 p-4 rounded-lg mb-6">
            {success}
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Article Form */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              {editingArticle ? "Επεξεργασία Άρθρου" : "Δημιουργία Νέου Άρθρου"}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Title */}
              <div>
                <label
                  htmlFor="title"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Τίτλος *
                </label>
                <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  required
                />
              </div>

              {/* Content */}
              <div>
                <label
                  htmlFor="content"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Περιεχόμενο * (HTML υποστηρίζεται)
                </label>
                <textarea
                  id="content"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={12}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-mono text-sm"
                  required
                />
              </div>

              {/* Labels */}
              <div>
                <label
                  htmlFor="labels"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Ετικέτες (χωρισμένες με κόμμα)
                </label>
                <input
                  type="text"
                  id="labels"
                  value={labels}
                  onChange={(e) => setLabels(e.target.value)}
                  placeholder="π.χ. Διατροφή, Υγεία, Βιταμίνες"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                />
              </div>

              {/* Category */}
              <div>
                <label
                  htmlFor="category"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Κατηγορία (Καρτέλα) *
                </label>
                <select
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white"
                  required
                >
                  {categories.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
                </select>
              </div>

              {/* Image Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Εικόνα (προαιρετικό)
                </label>
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                    isDragActive
                      ? "border-emerald-500 bg-emerald-50"
                      : "border-gray-300 hover:border-gray-400"
                  }`}
                >
                  <input {...getInputProps()} />
                  {imagePreview ? (
                    <div className="space-y-2">
                      <img
                        src={imagePreview}
                        alt="Preview"
                        className="max-h-40 mx-auto rounded"
                      />
                      <p className="text-sm text-gray-500">
                        Κάντε κλικ ή σύρετε για να αντικαταστήσετε
                      </p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-gray-600">
                        Σύρετε και αποθέστε μια εικόνα εδώ ή κάντε κλικ για επιλογή
                      </p>
                      <p className="text-sm text-gray-400 mt-1">
                        Max 5MB - JPEG, PNG, GIF, WebP
                      </p>
                    </div>
                  )}
                </div>
                {imagePreview && (
                  <button
                    type="button"
                    onClick={() => {
                      setImageFile(null);
                      setImagePreview(null);
                    }}
                    className="mt-2 text-sm text-red-600 hover:text-red-700"
                  >
                    Αφαίρεση εικόνας
                  </button>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting
                    ? "Αποθήκευση..."
                    : editingArticle
                    ? "Ενημέρωση Άρθρου"
                    : "Δημοσίευση Άρθρου"}
                </button>
                {editingArticle && (
                  <button
                    type="button"
                    onClick={clearForm}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Ακύρωση
                  </button>
                )}
              </div>
            </form>
          </div>

          {/* Articles List */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Δημοσιευμένα Άρθρα ({articles.length})
            </h2>

            {isLoading ? (
              <div className="text-center py-8 text-gray-500">Φόρτωση...</div>
            ) : articles.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                Δεν υπάρχουν άρθρα ακόμα. Δημιουργήστε το πρώτο σας άρθρο!
              </div>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto">
                {articles.map((article) => (
                  <div
                    key={article.id}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex gap-4">
                      {article.imageUrl && (
                        <img
                          src={article.imageUrl}
                          alt=""
                          className="w-20 h-20 object-cover rounded"
                        />
                      )}
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 truncate">
                          {article.title}
                        </h3>
                        <p className="text-sm text-gray-500 mt-1">
                          {new Date(article.published).toLocaleDateString(
                            "el-GR"
                          )}
                        </p>
                        {article.labels.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {article.labels.map((label) => (
                              <span
                                key={label}
                                className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded"
                              >
                                {label}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2 mt-3 pt-3 border-t border-gray-100">
                      <button
                        onClick={() => handleEdit(article)}
                        className="flex-1 text-sm text-emerald-600 hover:bg-emerald-50 px-3 py-2 rounded transition-colors font-medium"
                      >
                        ✏️ Επεξεργασία
                      </button>
                      <button
                        onClick={() => handleDelete(article.id)}
                        className="flex-1 text-sm text-red-600 hover:bg-red-50 px-3 py-2 rounded transition-colors font-medium"
                      >
                        🗑️ Διaγραφή
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

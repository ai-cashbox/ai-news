'use client';

import { useState, useEffect } from 'react';
import { RefreshCw, AlertCircle, FileText } from 'lucide-react';
import Header from '@/components/Header';
import ArticleCard from '@/components/ArticleCard';
import FilterBar from '@/components/FilterBar';
import Pagination from '@/components/Pagination';
import { articlesApi, Article, ArticleListResponse } from '@/lib/api';
import { useStore } from '@/lib/store';

export default function ArticlesPage() {
  const { filters } = useStore();
  const [data, setData] = useState<ArticleListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 20;

  const loadArticles = async (page: number = 1) => {
    setLoading(true);
    setError(null);
    try {
      const response = await articlesApi.getArticles({
        page,
        page_size: pageSize,
        category: filters.category || undefined,
        source: filters.source || undefined,
        min_score: filters.minScore || undefined,
        search: filters.search || undefined,
      });
      setData(response);
      setCurrentPage(page);
    } catch (err) {
      console.error('Failed to load articles:', err);
      setError('加载失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles(1);
  }, [filters]);

  const totalPages = data ? Math.ceil(data.total / pageSize) : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">全部资讯</h1>
          <p className="text-gray-500 mt-1">
            {data ? `共 ${data.total} 篇文章` : '加载中...'}
          </p>
        </div>

        {/* Filters */}
        <FilterBar />

        {/* Articles */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <RefreshCw className="w-10 h-10 text-primary-500 animate-spin mb-4" />
            <p className="text-gray-500">正在加载资讯...</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center py-20">
            <AlertCircle className="w-10 h-10 text-red-500 mb-4" />
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={() => loadArticles(currentPage)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              重新加载
            </button>
          </div>
        ) : !data || data.items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl">
            <FileText className="w-16 h-16 text-gray-300 mb-4" />
            <h3 className="text-xl font-medium text-gray-700 mb-2">没有找到文章</h3>
            <p className="text-gray-500">尝试调整筛选条件</p>
          </div>
        ) : (
          <>
            <div className="grid gap-6 md:grid-cols-2">
              {data.items.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>

            {/* Pagination */}
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={(page) => {
                loadArticles(page);
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
            />
          </>
        )}
      </main>
    </div>
  );
}

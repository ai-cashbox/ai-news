'use client';

import { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, RefreshCw, AlertCircle } from 'lucide-react';
import Header from '@/components/Header';
import ArticleCard from '@/components/ArticleCard';
import { articlesApi, Article } from '@/lib/api';
import dayjs from 'dayjs';

export default function HomePage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadArticles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await articlesApi.getTodayArticles(15, 50);
      setArticles(data);
    } catch (err) {
      console.error('Failed to load articles:', err);
      setError('加载失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="bg-gradient-to-br from-primary-500 via-primary-600 to-purple-600 rounded-2xl p-8 mb-8 text-white">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-6 h-6" />
            <span className="text-sm font-medium opacity-90">AI智能筛选</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold mb-3">
            今日AI热点
          </h1>
          <p className="text-lg opacity-90 mb-4">
            {dayjs().format('YYYY年MM月DD日')} · 为你精选最有价值的AI资讯
          </p>
          <div className="flex items-center gap-4 text-sm">
            <span className="flex items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              {articles.length} 篇精选
            </span>
            <button
              onClick={loadArticles}
              disabled={loading}
              className="flex items-center gap-1 hover:opacity-80 transition-opacity"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              刷新
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="text-2xl font-bold text-primary-600">
              {articles.filter((a) => a.quality_score >= 80).length}
            </div>
            <div className="text-sm text-gray-500">高质量文章</div>
          </div>
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="text-2xl font-bold text-green-600">
              {articles.filter((a) => a.source === 'arxiv').length}
            </div>
            <div className="text-sm text-gray-500">学术论文</div>
          </div>
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="text-2xl font-bold text-purple-600">
              {articles.filter((a) => a.category === 'llm').length}
            </div>
            <div className="text-sm text-gray-500">LLM相关</div>
          </div>
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="text-2xl font-bold text-orange-600">
              {articles.filter((a) => a.category === 'agent').length}
            </div>
            <div className="text-sm text-gray-500">Agent相关</div>
          </div>
        </div>

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
              onClick={loadArticles}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              重新加载
            </button>
          </div>
        ) : articles.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 bg-white rounded-xl">
            <Sparkles className="w-16 h-16 text-gray-300 mb-4" />
            <h3 className="text-xl font-medium text-gray-700 mb-2">暂无资讯</h3>
            <p className="text-gray-500 mb-4">系统正在采集最新的AI资讯</p>
            <p className="text-sm text-gray-400">
              提示：可以通过后台 API 触发爬虫采集数据
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2">
            {articles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p className="mb-2">AI News - 智能AI资讯聚合平台</p>
            <p>用AI筛选AI资讯，让你每天5分钟掌握最有价值的AI动态</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

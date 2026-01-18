'use client';

import { useState, useEffect } from 'react';
import { Filter, ChevronDown } from 'lucide-react';
import { articlesApi } from '@/lib/api';
import { useStore } from '@/lib/store';

interface Option {
  value: string;
  label: string;
}

export default function FilterBar() {
  const { filters, setFilters } = useStore();
  const [categories, setCategories] = useState<Option[]>([]);
  const [sources, setSources] = useState<Option[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [cats, srcs] = await Promise.all([
          articlesApi.getCategories(),
          articlesApi.getSources(),
        ]);
        setCategories(cats);
        setSources(srcs);
      } catch (error) {
        console.error('Failed to load filter options:', error);
      }
    };
    loadOptions();
  }, []);

  const categoryLabels: Record<string, string> = {
    llm: 'LLM',
    multimodal: '多模态',
    agent: 'Agent',
    cv: '计算机视觉',
    nlp: 'NLP',
    rl: '强化学习',
    robotics: '机器人',
    ai_safety: 'AI安全',
    business: '商业应用',
    other: '其他',
  };

  const sourceLabels: Record<string, string> = {
    arxiv: 'arXiv',
    openai_blog: 'OpenAI',
    google_ai_blog: 'Google AI',
    meta_ai_blog: 'Meta AI',
    techcrunch: 'TechCrunch',
    the_verge: 'The Verge',
    jiqizhixin: '机器之心',
    other: '其他',
  };

  const hasActiveFilters =
    filters.category || filters.source || filters.minScore > 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
      {/* Toggle Button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between w-full text-left"
      >
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-gray-500" />
          <span className="font-medium text-gray-700">筛选</span>
          {hasActiveFilters && (
            <span className="px-2 py-0.5 bg-primary-100 text-primary-700 rounded-full text-xs">
              已筛选
            </span>
          )}
        </div>
        <ChevronDown
          className={`w-5 h-5 text-gray-400 transition-transform ${
            isExpanded ? 'rotate-180' : ''
          }`}
        />
      </button>

      {/* Filter Options */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-gray-100 grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              分类
            </label>
            <select
              value={filters.category}
              onChange={(e) => setFilters({ category: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">全部分类</option>
              {categories.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {categoryLabels[cat.value] || cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Source */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              来源
            </label>
            <select
              value={filters.source}
              onChange={(e) => setFilters({ source: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">全部来源</option>
              {sources.map((src) => (
                <option key={src.value} value={src.value}>
                  {sourceLabels[src.value] || src.label}
                </option>
              ))}
            </select>
          </div>

          {/* Min Score */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              最低质量分: {filters.minScore}
            </label>
            <input
              type="range"
              min="0"
              max="90"
              step="10"
              value={filters.minScore}
              onChange={(e) => setFilters({ minScore: parseInt(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>0</span>
              <span>30</span>
              <span>60</span>
              <span>90</span>
            </div>
          </div>
        </div>
      )}

      {/* Clear Filters */}
      {hasActiveFilters && isExpanded && (
        <button
          onClick={() =>
            setFilters({ category: '', source: '', minScore: 0, search: '' })
          }
          className="mt-4 text-sm text-primary-600 hover:text-primary-700"
        >
          清除所有筛选
        </button>
      )}
    </div>
  );
}

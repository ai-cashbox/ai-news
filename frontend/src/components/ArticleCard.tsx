'use client';

import { ExternalLink, Star, Clock, User } from 'lucide-react';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/zh-cn';
import type { Article } from '@/lib/api';

dayjs.extend(relativeTime);
dayjs.locale('zh-cn');

interface ArticleCardProps {
  article: Article;
}

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

function getScoreColor(score: number): string {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  return 'bg-gray-400';
}

function getScoreBgColor(score: number): string {
  if (score >= 80) return 'bg-green-50 border-green-200';
  if (score >= 60) return 'bg-yellow-50 border-yellow-200';
  return 'bg-gray-50 border-gray-200';
}

export default function ArticleCard({ article }: ArticleCardProps) {
  const displayTitle = article.title_zh || article.title;
  const displaySummary = article.summary_zh || article.summary;
  const timeAgo = article.published_at
    ? dayjs(article.published_at).fromNow()
    : dayjs(article.crawled_at).fromNow();

  return (
    <article className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow animate-fade-in">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            {/* Quality Score */}
            <span
              className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium text-white ${getScoreColor(
                article.quality_score
              )}`}
            >
              <Star className="w-3 h-3" />
              {Math.round(article.quality_score)}
            </span>

            {/* Category */}
            <span className="px-2 py-1 bg-primary-50 text-primary-700 rounded-full text-xs font-medium">
              {categoryLabels[article.category] || article.category}
            </span>

            {/* Source */}
            <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
              {sourceLabels[article.source] || article.source}
            </span>
          </div>

          {/* External Link */}
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-shrink-0 p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
            title="查看原文"
          >
            <ExternalLink className="w-5 h-5" />
          </a>
        </div>

        {/* Title */}
        <h2 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-primary-600">
          <a href={article.url} target="_blank" rel="noopener noreferrer">
            {displayTitle}
          </a>
        </h2>

        {/* Original title if translated */}
        {article.title_zh && article.title !== article.title_zh && (
          <p className="text-sm text-gray-500 mb-2 line-clamp-1">{article.title}</p>
        )}

        {/* Summary */}
        {displaySummary && (
          <p className="text-gray-600 text-sm leading-relaxed mb-4 line-clamp-3">
            {displaySummary}
          </p>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-4">
            {/* Time */}
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {timeAgo}
            </span>

            {/* Authors */}
            {article.authors && article.authors.length > 0 && (
              <span className="flex items-center gap-1">
                <User className="w-4 h-4" />
                {article.authors.slice(0, 2).join(', ')}
                {article.authors.length > 2 && ` +${article.authors.length - 2}`}
              </span>
            )}
          </div>

          {/* Tags */}
          {article.tags && article.tags.length > 0 && (
            <div className="flex gap-1">
              {article.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </article>
  );
}

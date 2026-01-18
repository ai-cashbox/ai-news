'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { Settings, Mail, Bell, Filter, Save, Loader2, CheckCircle } from 'lucide-react';
import { usersApi } from '@/lib/api';
import { useStore } from '@/lib/store';

const categoryOptions = [
  { value: 'llm', label: 'LLM' },
  { value: 'multimodal', label: '多模态' },
  { value: 'agent', label: 'Agent' },
  { value: 'cv', label: '计算机视觉' },
  { value: 'nlp', label: 'NLP' },
  { value: 'rl', label: '强化学习' },
  { value: 'robotics', label: '机器人' },
  { value: 'ai_safety', label: 'AI安全' },
  { value: 'business', label: '商业应用' },
];

const frequencyOptions = [
  { value: 'realtime', label: '实时推送' },
  { value: 'daily', label: '每日精选' },
  { value: 'weekly', label: '每周汇总' },
];

export default function SettingsPage() {
  const router = useRouter();
  const { user, setUser, token } = useStore();
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  const [preferredCategories, setPreferredCategories] = useState<string[]>([]);
  const [minQualityScore, setMinQualityScore] = useState(60);
  const [emailFrequency, setEmailFrequency] = useState('daily');
  const [emailEnabled, setEmailEnabled] = useState(true);

  useEffect(() => {
    if (!token) {
      router.push('/login');
      return;
    }

    if (user) {
      setPreferredCategories(user.preferred_categories || []);
      setMinQualityScore(user.min_quality_score || 60);
      setEmailFrequency(user.email_frequency || 'daily');
      setEmailEnabled(user.email_enabled ?? true);
    }
  }, [user, token, router]);

  const handleCategoryToggle = (category: string) => {
    setPreferredCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
  };

  const handleSave = async () => {
    setLoading(true);
    setSaved(false);

    try {
      const updatedUser = await usersApi.updateMe({
        preferred_categories: preferredCategories,
        min_quality_score: minQualityScore,
        email_frequency: emailFrequency,
        email_enabled: emailEnabled,
      });
      setUser(updatedUser);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Failed to save settings:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Settings className="w-6 h-6" />
            个人设置
          </h1>
          <p className="text-gray-500 mt-1">自定义你的AI资讯偏好</p>
        </div>

        <div className="space-y-6">
          {/* Category Preferences */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
              <Filter className="w-5 h-5 text-primary-600" />
              关注领域
            </h2>
            <p className="text-sm text-gray-500 mb-4">
              选择你感兴趣的AI领域，系统会优先推送相关内容
            </p>
            <div className="flex flex-wrap gap-2">
              {categoryOptions.map((cat) => (
                <button
                  key={cat.value}
                  onClick={() => handleCategoryToggle(cat.value)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    preferredCategories.includes(cat.value)
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          {/* Quality Score */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
              <Bell className="w-5 h-5 text-primary-600" />
              质量门槛
            </h2>
            <p className="text-sm text-gray-500 mb-4">
              只推送质量评分高于此值的文章
            </p>
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">最低质量分</span>
                <span className="text-lg font-semibold text-primary-600">
                  {minQualityScore}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="90"
                step="10"
                value={minQualityScore}
                onChange={(e) => setMinQualityScore(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>全部</span>
                <span>30</span>
                <span>60</span>
                <span>90</span>
              </div>
            </div>
          </div>

          {/* Email Settings */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
              <Mail className="w-5 h-5 text-primary-600" />
              邮件订阅
            </h2>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">启用邮件推送</p>
                  <p className="text-sm text-gray-500">接收AI资讯邮件通知</p>
                </div>
                <button
                  onClick={() => setEmailEnabled(!emailEnabled)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    emailEnabled ? 'bg-primary-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      emailEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              {emailEnabled && (
                <div>
                  <p className="font-medium text-gray-900 mb-2">推送频率</p>
                  <div className="flex gap-2">
                    {frequencyOptions.map((freq) => (
                      <button
                        key={freq.value}
                        onClick={() => setEmailFrequency(freq.value)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          emailFrequency === freq.value
                            ? 'bg-primary-600 text-white'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {freq.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Save Button */}
          <div className="flex items-center gap-4">
            <button
              onClick={handleSave}
              disabled={loading}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Save className="w-5 h-5" />
              )}
              保存设置
            </button>

            {saved && (
              <span className="flex items-center gap-1 text-green-600">
                <CheckCircle className="w-5 h-5" />
                已保存
              </span>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

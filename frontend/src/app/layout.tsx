import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI News - 智能AI资讯聚合平台',
  description: '用AI筛选AI资讯，每天5分钟掌握最有价值的AI动态',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="bg-gray-50 min-h-screen">{children}</body>
    </html>
  );
}

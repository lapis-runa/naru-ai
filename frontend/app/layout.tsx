import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "なる専用思考AI",
  description: "自分の思考を保存し、構造化し、拡張する。しかし支配しない。",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja" suppressHydrationWarning>
      <head>
        {/* 明朝体（本文）とゴシック（UI部品）を読み込む */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;600&family=Noto+Serif+JP:wght@500;600&family=Zen+Kaku+Gothic+New:wght@400;500&display=swap"
          rel="stylesheet"
        />
        {/* テーマ初期化: 画面がちらつく前に、保存済みテーマを適用する */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var t = localStorage.getItem('naru-theme') || 'light';
                  document.documentElement.setAttribute('data-theme', t);
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
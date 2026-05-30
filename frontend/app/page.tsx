"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchRecent, type Entry } from "@/lib/api";

export default function Home() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // 起動時: 保存済みテーマを読み、日記一覧を取得
  useEffect(() => {
    const saved = (localStorage.getItem("naru-theme") as "light" | "dark") || "light";
    setTheme(saved);
    fetchRecent(50)
      .then(setEntries)
      .catch(() => setEntries([]))
      .finally(() => setLoading(false));
  }, []);

  function toggleTheme() {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("naru-theme", next);
  }

  return (
    <div className="container">
      <div className="topbar">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "☀ 昼" : "🌙 夜"}
        </button>
      </div>

      <header className="masthead">
        <h1 className="site-title">なる専用思考AI</h1>
        <p className="site-tagline">思考を保存し、構造化し、拡張する。しかし支配しない。</p>
      </header>

      <div className="mode-grid">
        <Link href="/write" className="mode-card">
          <div className="label">書く</div>
          <div className="sub">いま考えていることを</div>
        </Link>
        <Link href="/search" className="mode-card">
          <div className="label">探す</div>
          <div className="sub">言葉で・意味で</div>
        </Link>
      </div>

      <div className="section-head">これまでの記録</div>
      {loading ? (
        <p className="empty">読み込み中…</p>
      ) : entries.length === 0 ? (
        <p className="empty">まだ記録がありません。</p>
      ) : (
        <ul className="entry-list">
          {entries.map((e) => (
            <li key={e.id}>
              <Link href={`/entry/${e.id}`} className="entry-item">
                <span className="entry-title">{e.title || e.content.slice(0, 30)}</span>
                <span className="entry-date">{e.date}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}

      {/* AIと話す（枠だけ・中身は層2） */}
      <Link href="/chat" className="fab fab-ai">AI</Link>
    </div>
  );
}
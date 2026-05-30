"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { searchKeyword, searchSemantic, type SearchHit } from "@/lib/api";

export default function SearchPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"keyword" | "semantic">("semantic");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchHit[]>([]);
  const [searching, setSearching] = useState(false);
  const [searched, setSearched] = useState(false);

  async function handleSearch() {
    if (!query.trim()) return;
    setSearching(true);
    setSearched(true);
    try {
      const fn = mode === "keyword" ? searchKeyword : searchSemantic;
      setResults(await fn(query));
    } catch (e) {
      setResults([]);
    } finally {
      setSearching(false);
    }
  }

  return (
    <div className="container">
      <div className="edit-bar">
        <button className="bar-btn" onClick={() => router.push("/")}>← 戻る</button>
      </div>

      <div className="tabs">
        <button className={mode === "semantic" ? "tab active" : "tab"} onClick={() => setMode("semantic")}>
          意味で探す
        </button>
        <button className={mode === "keyword" ? "tab active" : "tab"} onClick={() => setMode("keyword")}>
          言葉で探す
        </button>
      </div>

      <input
        className="search-box"
        placeholder={mode === "semantic" ? "こんな気持ち・こんな話…" : "含まれる言葉…"}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
      />

      {searching ? (
        <p className="empty">探しています…</p>
      ) : searched && results.length === 0 ? (
        <p className="empty">見つかりませんでした。</p>
      ) : (
        <ul className="entry-list">
          {results.map((r) => (
            <li key={r.id}>
                <Link href={`/entry/${r.id}`} className="entry-item">
                <span className="entry-title">{r.title || r.snippet}</span>
                {r.score !== null && (
                    <span className="entry-score">{(r.score * 100).toFixed(0)}%</span>
                )}
                <span className="entry-date">{r.date}</span>
                </Link>
            </li>
            ))}
        </ul>
      )}
    </div>
  );
}
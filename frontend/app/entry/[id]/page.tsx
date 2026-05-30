"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchEntry, type Entry } from "@/lib/api";

export default function EntryPage() {
  const params = useParams();        // URLの [id] 部分を受け取る
  const router = useRouter();        // 戻る操作用
  const id = params.id as string;

  const [entry, setEntry] = useState<Entry | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetchEntry(id)
      .then(setEntry)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [id]);

  return (
    <div className="container">
      <a className="back-link read-back" onClick={() => router.back()}>
        ← 戻る
      </a>

      {loading ? (
        <p className="empty">読み込み中…</p>
      ) : error || !entry ? (
        <p className="empty">記事が見つかりませんでした。</p>
      ) : (
        <article>
          <h1 className="read-title">{entry.title || "(無題)"}</h1>
          <p className="read-date">{entry.date}　{entry.source}</p>
          <div className="read-body">{entry.content}</div>
        </article>
      )}
    </div>
  );
}
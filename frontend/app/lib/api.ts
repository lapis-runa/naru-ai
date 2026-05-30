// バックエンド(FastAPI, localhost:8000)と話す関数集。
// あなたのバックエンドのURL: /entries/(保存) /entries/recent(一覧) /entries/search(キーワード) /entries/semantic(意味)

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type Entry = {
  id: string;
  date: string;
  source: string;
  content: string;
  hash: string;
  title: string | null;
};

export type SearchHit = {
  id: string;
  date: string;
  source: string;
  title: string | null;
  snippet: string;
  score: number | null;
};

// 日付順の一覧 (ホーム画面)
export async function fetchRecent(limit = 50, offset = 0): Promise<Entry[]> {
  const res = await fetch(`${API}/entries/recent?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error("一覧の取得に失敗しました");
  return res.json();
}

// 日記を保存
export async function saveEntry(content: string, source: string, title?: string) {
  const res = await fetch(`${API}/entries/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content, source, title: title || null }),
  });
  if (!res.ok) throw new Error("保存に失敗しました");
  return res.json();
}

// キーワード検索
export async function searchKeyword(q: string): Promise<SearchHit[]> {
  const res = await fetch(`${API}/entries/search?q=${encodeURIComponent(q)}`);
  if (!res.ok) throw new Error("検索に失敗しました");
  return res.json();
}

// 意味検索
export async function searchSemantic(q: string): Promise<SearchHit[]> {
  const res = await fetch(`${API}/entries/semantic?q=${encodeURIComponent(q)}`);
  if (!res.ok) throw new Error("検索に失敗しました");
  return res.json();
}

// id指定で1件取得
export async function fetchEntry(id: string): Promise<Entry> {
  const res = await fetch(`${API}/entries/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error("記事の取得に失敗しました");
  return res.json();
}
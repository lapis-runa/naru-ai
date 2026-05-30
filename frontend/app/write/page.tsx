"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { saveEntry } from "@/lib/api";

const SOURCES = [
  { value: "diary", label: "日記" },
  { value: "creative", label: "創作" },
  { value: "memo", label: "メモ" },
  { value: "idea", label: "着想" },
];

export default function WritePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [source, setSource] = useState("diary");
  const [saving, setSaving] = useState(false);

  async function handleSave() {
    if (!content.trim()) return;
    setSaving(true);
    try {
      await saveEntry(content, source, title);
      router.push("/");          // 保存したらホームへ戻る
    } catch (e) {
      setSaving(false);
      alert("保存に失敗しました");
    }
  }

  return (
    <div className="container">
      <div className="edit-bar">
        <button className="bar-btn" onClick={() => router.push("/")}>
          キャンセル
        </button>
        <button className="bar-btn done" onClick={handleSave} disabled={saving || !content.trim()}>
          {saving ? "保存中…" : "完了"}
        </button>
      </div>

      <input
        className="editor-title"
        placeholder="タイトル"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="editor-body"
        placeholder="いま考えていることを、そのまま。"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <div className="edit-foot">
        <select className="select" value={source} onChange={(e) => setSource(e.target.value)}>
          {SOURCES.map((s) => (
            <option key={s.value} value={s.value}>{s.label}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
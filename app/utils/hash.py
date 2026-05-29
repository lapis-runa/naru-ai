"""
ハッシュ生成ユーティリティ。Raw層の改ざん検知用 SHA-256。
設計仕様書 2-1 / 7-3 準拠。

投入(import)でも新規保存(save)でも同じ計算を使うので、1か所にまとめる。
"""

import hashlib


def make_hash(id_: str, date: str, content: str) -> str:
    """id + date + content を連結し SHA-256 を取る。"sha256:..." 形式で返す。"""
    joined = id_ + date + content
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return "sha256:" + digest


def verify_hash(id_: str, date: str, content: str, stored_hash: str) -> bool:
    """保存済みハッシュと再計算が一致するか。不一致なら改ざんの疑い。"""
    return make_hash(id_, date, content) == stored_hash
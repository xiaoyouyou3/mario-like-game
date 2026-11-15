# KN-002 ローカルで配信したページが `/cdn/cp312/pygame_ce-...whl` を 404 で取得できない

| 項目 | 内容 |
|---|---|
| 分類 | ローカル配信 |
| 確度 | 確認済み |
| 関連 | REQ-105 |
| 記録日 | 2026-11-13 |

## 症状
ローカルで配信したページが `/cdn/cp312/pygame_ce-...whl` を 404 で取得できない

## 原因
pygbag のページは、ランタイムを `localhost:8000/cdn/...` から取りに来る。pygbag のテストサーバー（`testserver.py`）は、このパスを CDN へ中継してキャッシュする。単純な `python -m http.server` にはこの機能がない。

## 対処
`pygbag --bind 127.0.0.1 --port 8000 <フォルダ>` で配信する。フォルダ名が APK 名になる。公開用の静的配信（GitHub Pages）では、ページが CDN を直接参照するので、この問題は起きない。

## 再発防止
ローカル確認には pygbag のサーバーを使う。`http.server` を使わない。

## 根拠
`http.server` では 404、pygbag のサーバーに替えると 200（1,527,290 バイト）になった。`testserver.py` の `urlretrieve(CDN + self.path)` を確認。

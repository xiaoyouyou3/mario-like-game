# KN-006 ブラウザ操作ツールがない環境で、Web 版の読み込みを確認したい

| 項目 | 内容 |
|---|---|
| 分類 | 検証 |
| 確度 | 確認済み |
| 関連 | REQ-103 |
| 記録日 | 2026-11-13 |

## 症状
ブラウザ操作ツールがない環境で、Web 版の読み込みを確認したい

## 原因
built-in browser や Chrome 拡張のツールが使えなかった。ヘッドレス Chrome を使うと確認できるが、落とし穴が 3 つある。(1) macOS には `timeout` コマンドがない。(2) `--virtual-time-budget` は実時間のネットワーク待ちを待たずに終了する。(3) `--dump-dom` は load イベントの時点の DOM しか出さない。

## 対処
`--remote-debugging-port` で起動し、実時間で待ってから、CDP（標準ライブラリだけの簡易 WebSocket）で `Runtime.evaluate` を呼び、`infobox` の文字を読む。`--enable-logging=stderr` でコンソールログも取れる。終了は `kill`。

## 再発防止
実時間の挙動を見るときは、仮想時間と `--dump-dom` を使わない。画面の見た目は、画面外描画（`SDL_VIDEODRIVER=dummy`）で PNG に保存して `Read` で見る。

## 根拠
仮想時間では 2 秒で終了し `apk` 取得が出ず、実時間では `tar.gz` の取得まで進んだ。CDP で `infobox` が「Ready to start」になることを確認。

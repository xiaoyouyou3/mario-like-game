---
name: git-ops
description: Git の初期化・状態確認・ステージ・コミットを安全に行う。「コミットして」「Gitを初期化して」「履歴を残して」のときに使う。ユーザーが求めたときだけ実行する。
---

# Git 操作

## コミット手順
1. `git status` と `git diff --stat` で変更を確認する。`.venv/` `__pycache__/` `.pytest_cache/` が含まれていれば `.gitignore` を確認する。
2. **ファイルを名前で指定してステージ**する（`git add -A` / `git add .` は使わない）。
3. 直前に `run-tests` を実行する。コミット種別ごとの条件:
   | 種別 | 条件 |
   |---|---|
   | `test:` | 有効な Red（対象のみ失敗）であること。コミットメッセージに失敗の要点を書く |
   | `feat:` / `fix:` / `refactor:` | 全テスト緑 + ruff OK |
   | `docs:` / `chore:` | trace_check が OK（docs 変更時） |
4. メッセージ形式: `<type>: <TC-ID または対象> <要約>` ＋ 本文に1〜2行の理由。例: `test: TC-001..002 player horizontal acceleration (red: vel.x 0.0 != 12.0)`
5. 1コミット=1つの TC グループ工程（Red / Green / Refactor）。複数工程を混ぜない。

## 初期化
`git init -b main` → `.gitignore` 確認 → 初回コミットは `chore: scaffold harness and project skeleton`。

## 禁止・要確認
- 禁止: `push --force`、`reset --hard`、`clean -f`、`checkout .`、`--no-verify`、履歴書き換え。
- push・ブランチ削除・タグは、ユーザーの明示指示があるときだけ。
- 秘密情報（`.env`、キー）が差分にあれば中止して報告する。

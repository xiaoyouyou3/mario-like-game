# ナレッジ索引

セッションで起きた失敗・詰まり・見落としと、その対処を 1 件 1 ファイルで貯める。書き方と運用は `.claude/skills/knowledge/SKILL.md` と `.claude/rules/knowledge.md`。

作業の開始時に、この索引で該当する分類を探し、その件だけを読む（全件は読まない）。ID は欠番を詰めない。

## 分類
ビルド / ローカル配信 / Git / 検証 / 要件・設計の見落とし / レビュー / テスト / Claude の振る舞い

## 一覧
| ID | 分類 | 症状 | 確度 |
|---|---|---|---|
| [KN-001](KN-001-build-apk-bloat.md) | ビルド | APK が 29.5MB に肥大し、Web 版の読み込みが遅い | 確認済み |
| [KN-002](KN-002-pygbag-needs-testserver.md) | ローカル配信 | ローカルで配信したページが `/cdn/cp312/pygame_ce-...whl` を 404 で取得できない | 確認済み |
| [KN-003](KN-003-pygbag-first-load-stuck.md) | ローカル配信 | ページが「Loading, please wait ...」のまま止まる | 原因は推測・対処は確認済み |
| [KN-004](KN-004-browserfs-404-harmless.md) | ローカル配信 | コンソールに `//cdn/0.9.3//browserfs.min.js` の 404 が出続ける | 確認済み |
| [KN-005](KN-005-git-push-multi-account.md) | Git | `git push` が「Repository not found」になる | 確認済み |
| [KN-006](KN-006-headless-browser-verification.md) | 検証 | ブラウザ操作ツールがない環境で、Web 版の読み込みを確認したい | 確認済み |
| [KN-007](KN-007-ux-requirements-found-on-device.md) | 要件・設計の見落とし | スマホ実機で初めて 3 つの問題が見つかった | 確認済み |
| [KN-008](KN-008-review-rejects-and-stale-findings.md) | レビュー | 要件レビューが REJECT になった。レビュアーが古い数え方で指摘した | 確認済み |
| [KN-009](KN-009-mutation-check-for-first-pass-tests.md) | テスト | Red にしたとき、最初から通ってしまうテストがある | 確認済み |
| [KN-010](KN-010-claim-only-with-evidence.md) | Claude の振る舞い | 最初の説明で、実測前の推測を事実のように述べた | 確認済み |

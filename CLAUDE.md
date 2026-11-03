# Mario-like Game (pygame-ce)

スーパーマリオブラザーズ風の横スクロールアクション。TDD とコンテキストエンジニアリングの学習を兼ねる。

## コマンド
| 用途 | コマンド |
|---|---|
| 環境構築 | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` |
| テスト | `.venv/bin/pytest -q` |
| Lint | `.venv/bin/ruff check .` |
| トレーサビリティ検査 | `.venv/bin/python scripts/trace_check.py --stage spec\|tests\|all` |
| 起動 | `.venv/bin/python -m src.main` |

## 進め方
- 開発は `/dev-workflow` Skill が定義する工程表に従う。**最初に `docs/STATE.md` を読み、現在地から再開する。** 工程を進めたら STATE.md を更新する。
- 工程: 要件 → 基本設計 → テスト仕様 → [テスト(Red) → 実装(Green) → Refactor] の繰り返し。
- 詳細設計は作らない。テスト仕様書とテストコードが担う。
- 工程ごとの手順は Skill、守るべき基準は `.claude/rules/`（対象ファイルを触ると自動で読まれる）に書いてある。ここには重複して書かない。

## 絶対に守ること
1. テストより先に実装を書かない。Red（失敗）を実際に見てから実装する。
2. 失敗テストを消す・緩める・skip して通さない。
3. 要件定義と基本設計は、人間の承認なしに確定しない。
4. レビューは必ずサブエージェントに任せる。渡すのは成果物パス・上流文書パス・（再レビュー時）前回レビューのパスのみ。作成時の経緯や自己評価は渡さない。
5. 差戻し→再レビューは1工程につき最大2往復。超えたら作業を止めて人間に報告する。
6. 「通ったはず」と言わない。実行した出力を根拠にする。
7. 破壊的な Git 操作（`push --force`、`reset --hard`、`clean -f`）をしない。コミットはユーザーが求めたときだけ。

## ID 規約
`REQ-NNN`（要件）→ `DES-NNN`（設計、REQ を参照）→ `TC-NNN`（テストケース、REQ/DES を参照）→ テストコードに `# TC-NNN`。欠番は詰めない。

## 規約
Python 3.14 / 型ヒント必須 / 1ファイル1責務 / コミットは Conventional Commits。

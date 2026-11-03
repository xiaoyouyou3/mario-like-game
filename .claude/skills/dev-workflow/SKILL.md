---
name: dev-workflow
description: 開発全体の工程表（要件→設計→テスト仕様→TDDサイクル）を進行管理する。「開発を進めて」「次の工程は？」「続きから」「/dev-workflow」のとき、または新しいセッションの開始時に使う。docs/STATE.md を読んで現在地から再開する。
---

# 開発ワークフロー（親が実行する進行表）

**最初に必ず `docs/STATE.md` を読む。** 現在の工程と状態に該当する行から再開する。

## 工程表
| # | 工程 | 実行 | 成果物 | ゲート（次へ進む条件） | 差戻し先 |
|---|---|---|---|---|---|
| 1 | 要件定義 | `requirements` | docs/requirements/requirements.md | reviewer が APPROVE かつ **人間の承認** | 1 |
| 2 | 基本設計 | `basic-design` | docs/design/basic-design.md | reviewer が APPROVE かつ **人間の承認** | 2（要件の欠陥なら 1） |
| 3 | テスト仕様 | `test-spec` | docs/test-specs/test-spec.md | reviewer が APPROVE かつ `trace_check.py --stage spec` が OK | 3（設計の欠陥なら 2） |
| 4a | Red | `test-code` → `run-tests` | tests/test_*.py | **振る舞い不足で失敗**（`run-tests` が「有効なRed」と判定）かつ reviewer が APPROVE | 4a |
| 4b | Green | `implement` → `run-tests` | src/ | 対象テスト通過 **かつ** 全テスト通過 かつ ruff OK | 4b |
| 4c | Refactor | `implement`（Refactor節） | src/ | 全テスト通過を保ったまま | 4c |
| 4d | コードレビュー | `code-reviewer` | docs/reviews/ | APPROVE | 4b |
| 4e | 記録 | `git-ops`（ユーザー要求時） | コミット | - | - |
| 5 | 完了確認 | `run-tests` + `trace_check.py --stage all` | - | 全TC緑・ギャップ0・手動確認リスト提示 | 該当工程 |

4a〜4e は **TCグループ**（同じ振る舞いを扱う1〜5個のTC）単位で繰り返す。グループは test-spec の「グループ」列で決まる。

## レビュー依頼の作法（全工程共通）
1. サブエージェントに渡す: 成果物パス、上流文書パス、レビューファイルの保存先。再レビューなら前回レビューファイルのパス。
2. **渡さない**: 作成時の苦労・意図の説明・「ここは大丈夫なはず」といった自己評価。
3. 返答は判定 + Must 一覧 + ファイルパスのみ。詳細が必要なときだけレビューファイルを読む。

## 差戻しループ
- 判定が REJECT のとき: Must 指摘を修正 → STATE.md の往復を +1 → 前回レビューファイルを渡して再レビュー。
- **往復が 2 を超えたら停止**し、未解決 Must と原因の仮説を人間に報告して指示を待つ。
- 指摘に同意できないときは、勝手に無視せず根拠を添えて人間に判断を仰ぐ。

## STATE.md の更新タイミング
工程開始 / 成果物完成 / レビュー結果受領 / 人間の承認 / TDDグループの Red・Green・完了 / 停止時。更新は表の該当行の書き換えで行い、追記で履歴を肥大化させない。

## コンテキストの扱い
- 1工程が終わったら、次工程の前に `/clear` するか提案してよい（STATE.md と成果物があれば再開できる）。
- 大きな成果物は全文を会話に貼らず、パスで参照する。

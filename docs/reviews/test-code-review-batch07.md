# テストコードレビュー結果
- 対象: tests/test_interactions.py (TC-063〜077, TC-119) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md (DES-009) / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `.venv/bin/pytest -q tests/test_interactions.py` -> 32 failed, 4 passed。失敗は全て assert による AssertionError（ImportError/AttributeError なし）。通った 4 件は parametrize の一部（slide_age 0/11/12 の「死なない」と、SHELL_IDLE+WALKER の「何も起きない」）で、スタブの中立的な戻り値による。関数単位ではいずれも他のケースで失敗している。
  - `.venv/bin/python scripts/trace_check.py --stage tests` -> NG 一覧に TC-063〜077・TC-119 は含まれない（他バッチの TC のみ未実装）。
  - `.venv/bin/ruff check tests/test_interactions.py` -> 問題なし。
  - 非決定要素の grep（pygame, time, random, open, private 参照）-> 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | - | - | - | - | - |

## 確認した観点
| 観点 | 結果(✅/❌/—) | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 全失敗が AssertionError |
| TC 対応 | ✅ | TC-063〜077 と TC-119 に `# TC-NNN` 付きのテストあり。仕様外のテストなし |
| 仕様一致 | ✅ | 座標・vy・期待値（-200, 192, 200/-200, slide_age 閾値 12/13）が仕様書と一致 |
| アサーションの強さ | ✅ | 敵の alive、player_died、vy、y、state、vx を具体値で検証。踏みつけ不成立側も alive 真を検証 |
| 期待値の独立 | ✅ | 定数の再利用なし。手計算の直書き |
| 決定性 / 独立性 | ✅ | 各テストが自前でオブジェクトを生成。共有状態なし |
| 実装非依存 | ✅ | 公開属性のみ |
| 境界値 | ✅ | TC-064 (199.9/200.0/200.1), TC-075 (0,11,12,13,14,100), TC-119 の 3 点を parametrize / 2 テストで網羅 |
| 構造と命名 | ✅ | 振る舞いを表す名前。G-W-T が空行で分離 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装の正しさ | 対象外（Red 段階） | なし |

## 良い点
- 境界ケースの期待値が仕様書の根拠（216=208+16*0.5 等）と一致している。
- 踏みつけ不成立の側で alive と player_died の両方を確認しており、片側だけの実装ミスを検出できる。
- TC-072 / TC-076 でリスト順の両方を parametrize している。

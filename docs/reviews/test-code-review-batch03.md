# テストコードレビュー結果
- 対象: tests/test_tilemap.py (TC-017〜021) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `.venv/bin/pytest -q tests/test_tilemap.py` → 8 failed, 3 passed。失敗はすべて `assert False` 等の AssertionError（ImportError/AttributeError なし）。通過 3 件は EMPTY と上下端外が偽という中立スタブ(常に False/EMPTY)と一致するケースで、実装が正しくても間違っていても妥当な値。
  - `.venv/bin/python scripts/trace_check.py --stage tests` → TC-017〜021 の欠落報告なし（他バッチの TC は未実装のため NG）。
  - 非決定要素の grep（pygame, time, random, open）→ 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | - | - | - | - | - |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 8 件が AssertionError で失敗。スタブは中立値 |
| TC 対応 | ✅ | TC-017〜021 すべてに `# TC-NNN` あり、仕様外 TC なし |
| 仕様一致 | ✅ | EMPTY偽/SOLID・QUESTION・USED真、端 (-1,5)(200,5)真・(0,-1)(0,15)偽、戻り値と USED 化、非 QUESTION で不変、再生成で QUESTION を仕様どおり検証 |
| アサーションの強さ | ✅ | `is` による bool 厳密比較、タプルでの具体値比較。常に True/False を返す実装も落ちる |
| 期待値の独立 | ✅ | 直書きの具体値 |
| 決定性・独立性 | ✅ | テストごとに TileMap を新規生成、共有可変状態なし |
| 実装非依存 | ✅ | 公開メソッドと TileKind のみ使用 |
| 1テスト1振る舞い | ✅ | TC-020 は3回呼ぶが同一振る舞い（非QUESTIONは不変） |
| 境界値 | ✅ | TC-018 は仕様の4点を parametrize |
| 構造と命名 | ✅ | GWT が空行で分離、名前が振る舞いを表す |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装の正しさ | 対象外（Green 工程・code-reviewer） | なし |

## 良い点
- スタブが中立値で、失敗理由が純粋に振る舞いの不一致になっている。
- TC-021 で StageData の不変性も検証している。

# テストコードレビュー結果
- 対象: tests/test_player.py (TC-036〜049) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `.venv/bin/pytest -q tests/test_player.py`: 21 failed。すべて AssertionError（ImportError/AttributeError なし）。
  - `.venv/bin/python scripts/trace_check.py --stage tests`: TC-036〜049 に関する NG なし（他 TC の未実装ギャップのみ）。
  - 非決定要素の grep（pygame/time/random/open）: tests/test_player.py, tests/conftest.py ともに該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | - | - | - | - | - |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 21 件とも `assert 1.0 == 12` 等の AssertionError。スタブは `vx = 1.0` を設定する |
| TC 対応 | ✅ | TC-036〜049 の全てに `# TC-NNN` 付きテストがあり、範囲外の TC なし |
| 仕様一致 | ✅ | 期待値 12/90/-12/0,45/48/150/75/15,0,0/0/84/-330,202.5/-85,115/144.75/208.25,15,30 が仕様書と一致 |
| アサーションの強さ | ✅ | 具体値を approx で検証。TC-048 は (a)(b) 両方を parametrize。TC-049 は 12 回後と 13 回後の両方を検証 |
| 期待値の独立 | ✅ | 定数の再利用なし。手計算値の直書き |
| 決定性・独立性 | ✅ | dt 固定。テストごとに player と tilemap を生成し、共有状態なし |
| 実装非依存 | ✅ | 公開属性 (body.vx/vy/box/on_ground) のみ参照 |
| 1テスト1振る舞い | ✅ | TC-049 は仕様上の状態遷移 1 本で許容範囲 |
| 境界値 | ✅ | TC-037 と TC-043 は仕様どおりの 3 点 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装の正しさ | 対象外（Green 工程） | なし |

## 良い点
- 仕様の計算根拠どおりに期待値が手計算で書かれ、parametrize が仕様の点と一致している。

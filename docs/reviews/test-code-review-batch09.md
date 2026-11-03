# テストコードレビュー結果
- 対象: tests/test_level.py (TC-081〜091, TC-120〜122) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q tests/test_level.py -> 16 failed, 1 passed。失敗は全て AssertionError（ImportError/AttributeError なし）。passed 1 件は TC-091 の (100, 88.1, PLAYING) で、中立スタブの戻り値と偶然一致するだけで問題なし。trace_check --stage tests -> 対象 TC (081〜091, 120〜122) の NG なし（NG は対象外 TC のみ）。非決定要素の grep: 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | - | - | - | - | - |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 全失敗が AssertionError |
| TC 対応 | ✅ | 14 TC に対応する # TC-NNN 付きテストあり、余分な TC なし |
| 仕様一致 | ✅ | 配置・ステップ数・境界値(87.9/88.0/88.1/0、4回目/5回目、2回目/3回目、10/11回目、15/16回目)・期待値 224.5, 238, 242, 192, -200, 200 が仕様と一致 |
| アサーションの強さ | ✅ | 具体値、approx 使用、境界は前後を検証 |
| 期待値の独立 | ✅ | 手計算の直値 |
| 決定性・独立性 | ✅ | pygame/時間/乱数/ファイル不使用、テスト毎に Level を生成 |
| 実装非依存 | ✅ | 公開属性のみ（camera_x, tilemap.tile_at, enemies 等） |
| スタブの質 | ✅ | スタブは中立的な値（座標 0 など）で失敗理由を歪めていない |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装後の Green | Red 段階のレビューのため | なし |

## 良い点
- 境界を parametrize と段階別ステータス列で検証している。

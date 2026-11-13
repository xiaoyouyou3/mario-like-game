# テストコードレビュー結果
- 対象: tests/test_camera.py (G19), tests/test_render_pure.py (G26/G26b/G27/G27b), tests/test_constants.py (G27/G27b) / 上流: docs/test-specs/test-spec.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q 対象3ファイル -> 24 failed, 35 passed。失敗は全て AssertionError（ImportError/AttributeError なし）。trace_check --stage tests -> ギャップ 0 件。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| TEST-R-001 | new | Should | tests/test_render_pure.py TC-106 | 旧レイアウトが 592x304 内に収まるため、TC-106 は現状で最初から通る（Red にならない）。仕様の境界は 592/304 に緩んだだけなので許容範囲だが、実装が 256x240 のままでも検出できない。TC-123/125 が補完している。 | 対応不要。 |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 失敗は全て AssertionError |
| TC 対応 | ✅ | TC-080/106/111/113/116/123-128 全てにテストあり |
| 仕様一致 | ✅ | 期待値 (2608, 572, 2607, 592x304, 240/64, 48, 375/304, 0.0) が仕様と一致 |
| アサーションの強さ | ✅ | 具体値の比較。TC-124 は overlaps が辺接触を偽とする実装を確認 |
| 決定性・独立性 | ✅ | ウィンドウ・乱数・時刻なし |

## 未確認範囲
なし

# テストコードレビュー結果
- 対象: tests/test_input_state.py, tests/test_geometry.py, tests/test_constants.py / 上流: docs/test-specs/test-spec.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q 対象3ファイル -> 15 failed, 6 passed。失敗は全て AssertionError（スタブの中立値との不一致）。通った6件はスタブ値(False/空)と期待が偶然一致する parametrize の偽側ケースのみ。trace_check --stage tests の NG は対象外 TC の未作成のみ（TC-001〜006, 112, 113 は NG なし）。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | AssertionError のみ。Import/Attribute エラーなし |
| TC 対応 | ✅ | TC-001〜006,112,113 に # TC-NNN あり |
| 仕様一致 | ✅ | 期待値・パラメータが仕様書と一致 |
| アサーションの強さ | ✅ | 具体値の完全一致。is で bool 厳密比較 |
| 期待値の独立 | ✅ | 定数再利用なし |
| 決定性・独立性 | ✅ | pygame・乱数・時間・ファイル不使用 |
| 境界値 | ✅ | 接触(16)、半開区間、負値を網羅 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| TC-002 の「4通り」 | 検証対象は left/right/run の3項目で、jump は TC-001 が担う。仕様の期待値とも整合 | なし |

## 良い点
- 偽側ケースを含め、全項目の取り違えを検出できる

# テストコードレビュー結果
- 対象: tests/test_render_pure.py（G28: TC-129, 130, 131） / 上流: docs/test-specs/test-spec.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q tests/test_render_pure.py -> 7 failed, 42 passed。失敗 7 件は全て AssertionError（assert False is True / assert True is False）。trace_check --stage tests -> ギャップ 0 件。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 7 件全て AssertionError。ImportError なし |
| TC 対応 | ✅ | TC-129/130/131 に `# TC-NNN` あり。仕様外テストなし |
| 仕様一致 | ✅ | 穴 (10,14),(11,14)、col 9-12 の True/False/False/True、(20,13) のみ固体で False、col -1/200 で True。仕様どおり |
| アサーションの強さ | ✅ | `is expected` / `is True` / `is False` で具体値比較。row 13 を見る実装や外側を False にする実装は落ちる |
| 期待値の独立 | ✅ | 手計算の直書き |
| 決定性・独立性 | ✅ | ウィンドウ・乱数なし、状態共有なし |
| 構造と命名 | ✅ | Given/When/Then が空行で分離、名前が振る舞いを表す |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| なし | | |

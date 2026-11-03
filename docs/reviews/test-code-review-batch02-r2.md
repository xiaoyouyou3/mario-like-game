# テストコードレビュー結果 (batch02 再レビュー: G03 TC-007〜011 / G04 TC-012〜016)
- 対象: tests/test_stage_data.py, tests/conftest.py, src/game/stage_data.py(スタブ) / 上流: docs/test-specs/test-spec.md / 回: 2 (前回: test-code-review-batch02.md)
- 判定: APPROVE
- 実行したコマンド:
  - `.venv/bin/pytest -q tests/test_stage_data.py` -> 12 failed。TC-007〜011 は AssertionError(値の不一致)、TC-012〜016 は Failed: DID NOT RAISE StageFormatError。ImportError/IndexError なし。
  - `trace_check.py --stage tests` -> TC-007〜016 の欠落なし(NG は他バッチの TC のみ)。
  - 弱いアサーション/非決定性 grep -> 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| TEST-R-001 | resolved | Must | tests/test_stage_data.py:19-24, :61 / src/game/stage_data.py:31-34 | スタブが 16x200 の EMPTY を返す中立形になり、添字アクセスが成功。TC-007 は `EMPTY != SOLID`、TC-011 は `(16, 200) == (15, 200)` の AssertionError で落ちることを実行で確認。 | - |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 12 件すべて AssertionError / DID NOT RAISE |
| TC 対応 | ✅ | TC-007〜016 すべてに `# TC-NNN` |
| 仕様一致 | ✅ | 座標・期待値・match 文字列・parametrize(14/16、P 0/2)が仕様書と一致 |
| アサーションの強さ | ✅ | 具体値比較、具体例外型+match |
| 期待値の独立 | ✅ | 3168/160/16/48 は手計算の直書き |
| 決定性・独立性 | ✅ | 外部依存・共有状態なし |
| スタブの質 | ✅ | 中立値(全 EMPTY、(0,0))で期待値を返していない |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| Green 時の挙動 | 実装前 | なし |

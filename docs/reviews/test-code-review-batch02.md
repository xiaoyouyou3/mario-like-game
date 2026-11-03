# テストコードレビュー結果 (batch02: G03 TC-007〜011 / G04 TC-012〜016)
- 対象: tests/test_stage_data.py, tests/conftest.py / 上流: docs/test-specs/test-spec.md / 回: 1
- 判定: REJECT
- 実行したコマンド:
  - `.venv/bin/pytest -q tests/test_stage_data.py` -> 12 failed。TC-007 と TC-011 は IndexError、TC-008/009/010 は AssertionError、TC-012〜016 は Failed: DID NOT RAISE。
  - `trace_check.py --stage tests` -> 対象 TC-007〜016 の欠落報告なし。残りの NG は他バッチの TC。
  - 弱いアサーション grep -> 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| TEST-R-001 | new | Must | tests/test_stage_data.py:19-24 (TC-007), :61 (TC-011) | 有効な Red でない。スタブは `tiles=()` を返すので、`data.tiles[14][3]` と `data.tiles[0]` が IndexError になる（実行確認済み）。AssertionError ではなく、期待値と実際値の比較まで到達していない。 | 添字アクセスより前にアサーションで落とす。TC-011 は `len(data.tiles)` を先に評価し、`tiles[0]` を触らない形にする（例: `(len(data.tiles), {len(r) for r in data.tiles})` を `(15, {200})` と比較）。TC-007 は `data.tiles` 全体から SOLID/QUESTION/EMPTY のマスを取り出す形にするか、スタブを中立な形（15x200 の EMPTY）にする。 |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ❌ | TC-007/011 が IndexError。他 10 件は AssertionError / DID NOT RAISE で有効。 |
| TC 対応 | ✅ | TC-007〜016 すべてに `# TC-NNN` あり。仕様外のテストなし。 |
| 仕様一致 | ✅ | 座標、期待値、match 文字列、parametrize（14/16 行、P 0/2 個）が仕様書と一致。 |
| アサーションの強さ | ✅ | 具体値の比較と、match 付きの具体的な例外型。実装ミスは検出できる。 |
| 期待値の独立 | ✅ | 3168/160/16/48 は手計算の直書き。 |
| 決定性・独立性 | ✅ | pygame、乱数、ファイル、時間への依存なし。共有の可変状態なし。 |
| 1テスト1振る舞い | ✅ | TC-007 は 1 振る舞い（文字からタイル種別への対応）で、5 値の組をまとめて比較している。 |
| 構造と命名 | ✅ | Given/When/Then が空行で分かれ、名前が振る舞いを表している。 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装が正しいときの Green | 実装前のため | なし |

## 良い点
- 異常系はすべて `StageFormatError` と `match=` を指定している。
- conftest の `stage_text` で P/F の重複配置を制御できていて、TC-015 の 0 個と 2 個を作り分けられる。

# コードレビュー結果 (batch02)
- 対象: src/game/stage_data.py, src/game/constants.py / 上流: docs/test-specs/test-spec.md (TC-007〜016), docs/design/basic-design.md (DES-004), docs/requirements/requirements.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q (33 passed), ruff check (All checks passed), grep pygame src/game (0件), 危険API grep (0件), 実時間/乱数 grep (0件)

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| (なし) | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 一般式の解析のみ。直書き・テスト専用分岐なし |
| 仕様適合 | ✅ | TC-007〜016 の各例外メッセージ(width/height/unknown character/start/flag)と旗 Aabb 計算が仕様と一致 |
| 過剰実装 | ✅ | 仕様外の機能なし |
| 層の分離 | ✅ | pygame・実時間・乱数・ファイルアクセスなし |
| 定数 | ✅ | 寸法は constants.py に集約 |
| 入力検証 | ✅ | 幅・高さ・未知文字・P個数・F有無を StageFormatError で検証 |
| 危険API/例外処理 | ✅ | 該当なし |
| 型/構造 | ✅ | 型ヒントあり、関数は短い |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| assets/stages/stage1.txt との整合 | 対象外 (DES-019) | なし |

## 良い点
- 検証と変換が小関数に分かれ、例外メッセージが仕様の match と一致している。

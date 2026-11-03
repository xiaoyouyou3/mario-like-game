# コードレビュー結果
- 対象: src/game/tilemap.py / 上流: docs/test-specs/test-spec.md (TC-017〜021), docs/design/basic-design.md (DES-005) / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q (44 passed), ruff check . (All checks passed), grep pygame/time/random/危険API (src/game 0件), マジックナンバー grep (tilemap.py に該当なし)

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| (なし) | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 一般式のみ。値の直書き・テスト専用分岐なし |
| 仕様適合 | ✅ | 左右端=壁(真)、上下の外=空(偽)、USED も固体。TC-018 と一致 |
| 過剰実装 | ✅ | 設計の3メソッド+is_solid のみ |
| 層の分離 | ✅ | pygame・時間・乱数・ファイルなし |
| 設計一致 | ✅ | StageData から list へ複製し、不変の StageData を変更しない (TC-021) |
| 危険API・例外処理 | ✅ | 該当なし |
| 数値の頑健性 | ✅ | 整数インデックスのみ。is_solid は範囲外を処理済み |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| tile_at/hit_question の範囲外/負インデックス | is_solid が偽を返す行では天井セルが生じないため呼び出し側から到達しない見込み。Level 未実装で確認不能 | なし |

## 良い点
- 責務が小さく設計どおり。複製により StageData の不変性を保っている。

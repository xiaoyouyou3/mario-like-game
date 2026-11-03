# コードレビュー結果 (batch09 level)
- 対象: src/game/level.py, src/game/constants.py / 上流: docs/test-specs/test-spec.md (TC-081〜091, 120〜122), docs/design/basic-design.md (DES-011, §5) / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q = 182 passed / ruff = All checks passed / grep pygame・実時間・乱数・危険API = 0件 / マジックナンバー grep は level.py に該当なし

## 指摘
なし

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 一般式のみ。直書き・テスト専用分岐なし |
| 仕様適合 | ✅ | §5 の手順3〜10の順と一致。判定はカメラ更新前の値、死亡優先、PLAYING 以外は進めない |
| 過剰実装 | ✅ | 仕様外の機能なし |
| 層の分離 | ✅ | 純Python |
| 定数 | ✅ | PLAYER_START_OFFSET_X 等は constants.py |
| 数値の頑健性 | ✅ | ceiling_cell は固体セルのみで row 範囲内、hit_question の負添字は起きない |
| 構造・型 | ✅ | 関数は短く型ヒントあり |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 描画・Session 連携 | 対象外 | なし |

# コードレビュー結果 (batch05)
- 対象: src/game/player.py (関連 src/game/constants.py) / 上流: docs/test-specs/test-spec.md (TC-036〜049, §0), docs/design/basic-design.md (DES-007) / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q = 89 passed / ruff check = All checks passed / grep pygame, 実時間, 乱数, 危険API = 0件

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| CODE-R-001 | new | Should | src/game/player.py:21-22 | PLAYER_W/PLAYER_H が player.py に定義。basic-design.md の定数表(268-269行)は constants に集約する前提で、他の寸法と置き場が不一致。他モジュール(敵・interactions)が参照する際に player への依存や重複定義が生じうる | constants.py に移す |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | dt・値の直書き分岐なし。一般式 |
| 仕様適合 | ✅ | §0 の (1)(2)(3) と ACCEL/DECEL/max が一致。ジャンプは接地時のみ vy=-JUMP_SPEED の後に重力 (TC-046 の -330) |
| 過剰実装 | ✅ | 仕様外の分岐なし |
| 層の分離 | ✅ | grep 0件 |
| 定数 | ✅(Should 1件) | 速度・加速度は constants 集約 |
| 型 | ✅ | 型ヒントあり |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 大 dt の頑健性 | move_and_collide は player.py の範囲外 | なし |

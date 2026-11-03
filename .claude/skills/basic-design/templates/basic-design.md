# 基本設計書

最終更新: YYYY-MM-DD / 状態: ドラフト | レビュー中 | 承認済 / 対応要件: requirements.md

## 1. 要件割当表（空欄禁止）
| REQ | 担当 DES | 備考 |
|---|---|---|
| REQ-001 | DES-001 | |

## 2. データモデル
| 名前 | 場所 | 属性（型・単位） | 持ち主 |
|---|---|---|---|
| Player | src/game/player.py | pos: Vec2(px), vel: Vec2(px/s), on_ground: bool, state: PlayerState | World |

## 3. モジュール責務
| ID | モジュール | 責務（1文） | 依存してよいもの | 対応REQ |
|---|---|---|---|---|
| DES-001 | src/game/player.py | 入力と時間から Player の速度・位置を更新する | constants, InputState | REQ-001, REQ-002 |

## 4. インターフェース
```python
# 例: シグネチャと入出力の意味だけ。本体は書かない
def update_player(player: Player, inp: InputState, dt: float) -> None:
    """player を dt 秒進める。副作用: player.pos/vel/on_ground を更新"""
```

## 5. 1フレームの更新順序
1. 入力取得（render層） → 2. プレイヤー更新 → 3. 敵更新 → 4. 衝突解決 → 5. 勝敗判定 → 6. カメラ更新 → 7. 描画

## 6. 定数表（`src/game/constants.py` に集約）
| 名前 | 値 | 単位 | 出典 |
|---|---|---|---|
| GRAVITY | 900 | px/s^2 | 初期値案 |

## 7. 設計判断
| # | 選択 | 代替案 | 理由 |
|---|---|---|---|

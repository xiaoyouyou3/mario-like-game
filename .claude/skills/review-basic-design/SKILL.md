---
name: review-basic-design
description: 基本設計書のレビュー基準表と検証コマンド。basic-design-reviewer サブエージェントが review-common と合わせて使う。
---

# 基本設計レビュー基準

入力: `docs/design/basic-design.md`、上流 `docs/requirements/requirements.md`。IDプレフィックス: `DES-R`。

## 先に実行する検証コマンド
```bash
R() { grep -oE "REQ-[0-9]+" "$1" | sort -u; }
comm -23 <(R docs/requirements/requirements.md) <(R docs/design/basic-design.md)   # 設計に割り当てられていない REQ
comm -13 <(R docs/requirements/requirements.md) <(R docs/design/basic-design.md)   # 存在しない REQ への参照
grep -nE "pygame" docs/design/basic-design.md                                       # 出現箇所が render 層だけか確認
```

## 基準表（✕ は Must）
| 観点 | 合格基準 | Must にする例 |
|---|---|---|
| 要件カバー | 割当表で全 REQ が DES に紐づく。REQ に紐づかない DES がない | REQ-005 がどの DES にも割り当てられていない |
| 層の分離 | `src/game/` のモジュールが pygame・実時間・ファイルに依存しない記述 | `game/player.py` が `pygame.key` を読む設計 |
| 依存方向 | `main → render → game` の一方向。循環がない | `game` が `render` を import する |
| テスト容易性 | 時間は `dt`、乱数は注入、入力は `InputState` で渡す | `update()` 内で `time.time()` を使う設計 |
| 状態の持ち主 | 各データの持ち主が1か所。同じ状態が複数モジュールに重複しない | `on_ground` を Player と World の両方が保持 |
| インターフェース | シグネチャ・単位・副作用が書かれている | 引数の単位（px か タイルか）が不明 |
| 更新順序 | 1フレームの更新順序が明記され、衝突解決の前後関係に矛盾がない | 衝突解決後にプレイヤー速度を更新している |
| 定数表 | 全定数に値・単位・出典。マジックナンバーが本文にない | 本文に「約 90」とあるが定数表にない |
| 設計判断 | 重要な選択に代替案と理由がある | 衝突方式を選んだ理由がない（Should） |
| 実現性 | pygame-ce と Python 3.14 で実現可能 | 使えないAPIを前提にしている |
| スコープ | 要件にない機能の設計がない | 要件にないパワーアップ用クラス（過剰設計） |
| 詳細度 | 関数本体・疑似コードが書かれていない | アルゴリズムの擬似コードが設計書に書かれている（Should） |

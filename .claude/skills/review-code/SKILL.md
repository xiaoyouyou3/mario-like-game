---
name: review-code
description: 実装コード（src/）のレビュー基準表と検証コマンド。TDDではテストが通っても残る「迎合・過剰実装・設計逸脱・セキュリティ」を見る。code-reviewer サブエージェントが review-common と合わせて使う。
---

# コードレビュー基準

入力: 対象 `src/` のパス（または差分）、上流 `docs/test-specs/test-spec.md` `docs/design/basic-design.md`、対応する `tests/`。IDプレフィックス: `CODE-R`。基準の正本は `.claude/rules/architecture.md`。

テストが通ることは前提。**テストが保証しないこと**を見る。

## 先に実行する検証コマンド
```bash
.venv/bin/pytest -q && .venv/bin/ruff check .                                   # 緑であること
grep -rn "pygame" src/game                                                       # 0件であること
grep -rnE "time\.(time|sleep)|import random|random\.(random|randint|choice)" src/game   # 実時間・グローバル乱数
grep -rnE "eval\(|exec\(|pickle|yaml\.load\(|os\.system|subprocess|__import__" src       # 危険API
grep -rnE "\b[0-9]+\.[0-9]+\b|\b[0-9]{3,}\b" src/game --include=*.py | grep -v constants.py   # マジックナンバー候補
git diff --stat 2>/dev/null | tail -1                                           # 変更規模（gitがあれば）
```

## 基準表（✕ は Must）
| 観点 | 合格基準 | Must にする例 |
|---|---|---|
| テスト迎合 | テスト値の直書き・テスト専用分岐・期待値の丸写しがない。仕様書の別 TC（境界など）でも成り立つ一般式になっている | `if dt == 1/60: return 12.0` |
| 仕様適合 | 対象 TC の振る舞いが、仕様書の備考（定数・計算根拠）と一致して実装されている | 仕様の ACCEL=720 と異なる値で、偶然テストを通している |
| 過剰実装 | 仕様書にない機能・引数・分岐・フォールバックがない | 要件にない二段ジャンプの処理 |
| 層の分離 | `src/game/` に pygame・実時間・グローバル乱数・ファイルアクセスがない | `game/` で `import pygame` |
| 設計一致 | 基本設計の責務・インターフェース・更新順序・状態の持ち主と一致する | 設計にない場所に状態を複製 |
| 定数 | マジックナンバーが `constants.py` に名前付き・単位コメントつきで集約 | 本体に `0.08` が直書き |
| 入力検証 | 外部データ（ステージファイル等）の形式・範囲を検証し、具体的な例外を出す | 不正なステージ文字で IndexError |
| 危険API | eval/exec/pickle/unsafe yaml/os.system/パス結合の未検証がない | ステージ名をそのままファイルパスに結合 |
| 例外処理 | 裸の `except:`・握りつぶし（`except Exception: pass`）がない | 失敗を無言で無視 |
| 数値の頑健性 | 大きな `dt` でもすり抜けない。ゼロ除算・負の座標の `int()` 丸めがない | 大きな dt で壁を貫通 |
| 型 | 公開関数に型ヒント。`Any` なし | 戻り値型の欠落（Should） |
| 構造 | 関数 50 行以内・引数 5 個以内・ネスト 3 段以内・重複なし | 100行の update（Should） |
| 命名・一貫性 | 既存コードの規約と一致 | （Should） |
| 死んだコード | 未使用の関数・変数・import がない | （Should。ruff が拾うものは ruff に任せる） |

## 判定の注意
- 「好みのリファクタ案」は書かない。保守性の指摘は、具体的な将来の失敗（変更時に何が壊れるか）を書けるものだけ。
- 描画層（`src/render/`, `src/main.py`）は自動テスト対象外。層の分離とロジック漏れ（ルール判断が入っていないか）だけ見る。

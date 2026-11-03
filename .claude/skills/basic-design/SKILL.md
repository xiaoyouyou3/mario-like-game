---
name: basic-design
description: 承認済みの要件定義書から基本設計書（モジュール構成・データモデル・インターフェース・1フレームの更新順序・定数表）を作成・更新する。「設計して」「モジュール構成を決めたい」のときに使う。成果物は docs/design/basic-design.md。
---

# 基本設計

基準は `.claude/rules/docs.md` と `.claude/rules/architecture.md`。ゲーム固有の数値・アルゴリズムの定石は [../implement/references/game-knowledge.md](../implement/references/game-knowledge.md) を参照する。

## 前提チェック（満たさなければ中断して人間に確認）
- `docs/STATE.md` の承認ログで要件定義書が「承認済」である。
- requirements.md の未決事項が空、または設計に影響しないと人間が確認済み。

## 手順
1. requirements.md を読み、全 REQ を一覧化する。
2. [templates/basic-design.md](templates/basic-design.md) に沿って書く。順序は **データモデル → モジュール責務 → インターフェース → 更新順序 → 定数表 → 設計判断**。
3. **割当表**を作る: 全 REQ がどの DES に担われるかを表にし、空欄がないことを確認する。
4. 設計判断（ADR簡易版）は「選択 / 代替案 / 理由」の3点を1件ずつ書く。選ぶ理由が書けないものは判断として書かない。
5. セルフチェック:
   - `src/game/` 配下に置くモジュールの記述に pygame が登場しない
   - 各インターフェースの時間・乱数・入力が引数で渡る形になっている
   - 定数表の全定数に単位と出典（要件ID または「初期値案」）がある
6. STATE.md を更新し、人間に承認を依頼する（レビューは `basic-design-reviewer`）。

## 書かないもの
関数本体・疑似コード・テストケース（テスト仕様書の役割）・要件にない機能。

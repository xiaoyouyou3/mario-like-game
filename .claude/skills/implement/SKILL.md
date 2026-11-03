---
name: implement
description: 有効な Red のテストを通す最小実装（Green）を書き、テストが緑のままリファクタリングする（Refactor）。TDD の Green/Refactor フェーズ。「実装して」「テストを通して」のときに使う。ゲームの数値・衝突処理の定石は references/game-knowledge.md。
---

# 実装（Green → Refactor）

基準は `.claude/rules/architecture.md`。物理・衝突・カメラの定石は [references/game-knowledge.md](references/game-knowledge.md)。

## 前提チェック
- 対象 TC グループが **有効な Red**（AssertionError で失敗）と STATE.md / tdd-log に記録されている。なければ `test-code` に戻る。

## Green
1. 変更予定を宣言する（作成/変更するファイルと理由を3行以内。`docs/evidence/tdd-log.md` の該当行に追記）。
2. **失敗しているテストを通す最小のコード**だけを書く。仕様書にない機能・引数・分岐を足さない。
3. 定数は `constants.py` に名前付きで置く。仕様書の備考にある値（例: ACCEL=720）と一致させる。
4. `run-tests`: 対象テストが通り、**全テスト**が通り、`ruff check` が OK であること。

### 近道の禁止（テストへの迎合）
- テスト値の直書き（`if x == 12.0: return ...`）、テスト専用の分岐、期待値の丸写しは禁止。
- 複数の入力で成り立つ一般式で書く。迷ったら、仕様書の別の TC（境界など）でも通るかを頭の中で確かめる。

## Refactor
テストが緑のまま、1変更ごとに `run-tests` を回す。見る点: 重複 / 命名 / 関数の長さ（50行）/ 責務 / マジックナンバー。新しい振る舞いを足さない。

## グループ完了時
1. `docs/evidence/tdd-log.md` に Green/Refactor の結果（変更ファイルと全テスト件数）を記録。
2. セルフチェック: `grep -rn "pygame" src/game` が 0 件 / `ruff` OK / 全テスト緑。
3. STATE.md を更新し、`code-reviewer` にレビューさせる。

## 詰まったとき
同じテストが 3 回連続で通らない場合、実装を足し続けず、(a) テストの期待値が仕様書とずれていないか (b) 仕様書の計算根拠が正しいか を確認する。仕様書側の誤りなら `test-spec` に差戻す。

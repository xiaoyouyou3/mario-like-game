---
name: test-code
description: テスト仕様書の1つのTCグループを pytest のテストコードにし、有効な Red（振る舞い不足による失敗）まで持っていく。TDD の Red フェーズ。「テストを書いて」「次のTCグループ」のときに使う。実装コードは書かない。
---

# テストコード作成（Red）

基準は `.claude/rules/testing.md`。

## 手順
1. `docs/STATE.md` の TDD 進捗から次の **TCグループ** を選ぶ。1回に扱うのは1グループ（1〜5 TC）。
2. `tests/test_<module>.py` に書く。TC 1つにつきテスト関数 1つ（境界値は `parametrize` 可）。
   ```python
   # TC-001
   def test_player_accelerates_right_by_one_frame_when_right_pressed() -> None:
       player = Player(pos=Vec2(0, 0), on_ground=True)          # Given

       update_player(player, InputState(right=True), dt=1 / 60)  # When

       assert player.vel.x == pytest.approx(12.0)                # Then (ACCEL 720 * 1/60)
   ```
   - テスト名は「主語_振る舞い_条件」の英語スネークケース。
   - 期待値は仕様書の備考にある手計算値を直書きする（定数の再利用で計算しない）。
3. **スタブを最小限作る**（モジュールがまだ無い場合）: クラスと関数のシグネチャだけを作り、戻り値は中立値（0 / None / 空）にする。`raise NotImplementedError` や `pass` で ImportError/例外を起こすのではなく、**テストがアサーションで落ちる**状態にする。
4. `run-tests` Skill で対象だけ実行し、**有効な Red** であることを確認する。
5. `docs/evidence/tdd-log.md` に TC・失敗メッセージの要点を記録する（[../run-tests/SKILL.md](../run-tests/SKILL.md) の形式）。
6. STATE.md を更新し、`test-code-reviewer` にレビューさせる。

## 有効な Red の判定
| 失敗の種類 | 判定 | 対処 |
|---|---|---|
| `AssertionError`（期待値と実際値が違う） | 有効 | 次へ |
| `ImportError` / `ModuleNotFoundError` / `AttributeError` / `TypeError`（引数） / `SyntaxError` / `NameError` | 無効（環境・構造の問題） | スタブかテストを直す |
| 最初から Pass | 無効（テストが弱い / 既に実装済み） | テストを疑い、アサーションを強める |

## 禁止
- 実装コード（スタブ以外）を書く。
- 仕様書にない TC を勝手に足す（必要なら先に仕様書を更新）。
- pygame のウィンドウ・実時間・乱数・ファイルに依存するテスト。

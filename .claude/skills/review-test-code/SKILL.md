---
name: review-test-code
description: テストコード（tests/）のレビュー基準表と検証コマンド。test-code-reviewer サブエージェントが review-common と合わせて使う。
---

# テストコードレビュー基準

入力: 対象の `tests/test_*.py` と対象 TC グループ、上流 `docs/test-specs/test-spec.md`。IDプレフィックス: `TEST-R`。基準の正本は `.claude/rules/testing.md`。

## 先に実行する検証コマンド
```bash
.venv/bin/pytest -q <対象>                                 # Red の失敗理由を自分で確認する
.venv/bin/python scripts/trace_check.py --stage tests       # TC とテストの対応
grep -nE "^\s*assert [a-z_\.]+$|is not None$|pytest\.raises\(Exception" tests/*.py   # 弱いアサーション候補
grep -nE "import pygame|time\.(sleep|time)|random\.|open\(" tests/*.py               # 非決定的・環境依存の候補
```

## 基準表（✕ は Must）
| 観点 | 合格基準 | Must にする例 |
|---|---|---|
| 有効な Red | 対象は `AssertionError` で失敗している（自分で実行して確認） | ImportError/AttributeError で落ちている、または最初から通る |
| TC 対応 | 対象 TC 全てに `# TC-NNN` 付きのテストがあり、仕様書にない TC がない | TC-003 のテストが存在しない |
| 仕様一致 | Given/When/Then と期待値が仕様書と一致 | 仕様は 12.0、テストは 10.0 |
| アサーションの強さ | 実装が間違っていたら落ちる。期待値は手計算の具体値 | `assert player.vel.x > 0` のみで上限を検証していない |
| 期待値の独立 | 期待値が実装・定数の式の再利用でない | `assert v == ACCEL * dt`（定数を再利用） |
| 決定性 | 実時間・乱数・ウィンドウ・ファイルに依存しない | `time.sleep` や `pygame.init()` を使う |
| 独立性 | テスト間で状態を共有しない（モジュールレベルの可変オブジェクト等） | グローバルの Player を複数テストで共有 |
| 実装非依存 | 公開された振る舞いのみ検証する | `_private` 属性やメソッド呼び出し回数を検証 |
| 1テスト1振る舞い | When が1つ。アサーションが同一の振る舞い | 1テストでジャンプと着地の両方を検証 |
| 構造と命名 | Given/When/Then が空行で分かれ、名前が振る舞いを表す | `test_1` `test_player` |
| 境界値 | 閾値は parametrize で3点を検証 | 仕様が3点なのに1点のみ |
| スタブの質 | スタブは中立値を返し、テストの失敗理由を歪めない | スタブがテストの期待値を返している |

## 判定の注意
- 実装コードの良し悪しは対象外（code-reviewer の役割）。
- テストの追加要求は、仕様書の TC に根拠がある場合のみ。仕様外の追加テストを要求しない。

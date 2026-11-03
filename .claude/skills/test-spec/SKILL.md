---
name: test-spec
description: 要件と基本設計からテスト仕様書（テストケース一覧）を作成・更新する。TDDでは詳細設計を兼ねる。「テストケースを洗い出して」「テスト仕様を書いて」のときに使う。成果物は docs/test-specs/test-spec.md。
---

# テスト仕様書（= 詳細設計）

基準は `.claude/rules/testing.md`。このドキュメントを読めば、テストコードと実装が書ける粒度にする。

## 手順
1. requirements.md の受入条件と、basic-design.md の各 DES を読む。
2. DES ごとに、[references/techniques.md](references/techniques.md) の技法で TC を導出する（正常系 → 境界 → 異常 → 状態遷移の順）。
3. [templates/test-spec.md](templates/test-spec.md) の表に書く。
   - Given/When/Then は **具体的な数値** で書く。「速い」「正しく」は禁止。
   - 期待値は手計算できる値にする。計算過程を備考に書く（例: `v = 900 * (1/60) = 15`）。
   - TC を **グループ**（同じ振る舞いを扱う1〜5個）にまとめる。TDD 1サイクルはこの単位。
4. 自動テストにできないもの（描画の見た目・操作感）は表末尾の「手動確認」に分離する。
5. 検査: `.venv/bin/python scripts/trace_check.py --stage spec` が OK（全 REQ が TC に紐づく）。
6. STATE.md を更新し、`test-spec-reviewer` にレビューさせる。

## 禁止
- 期待結果が「正常に動作する」「エラーにならない」のみ。
- 1 TC に複数の振る舞いを入れる（When が2つ以上、Then が無関係な2つ以上）。
- 実装の内部変数名を期待結果にする（公開インターフェースで観測できる値にする）。

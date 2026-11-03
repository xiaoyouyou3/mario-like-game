# テストコードレビュー結果 (batch10)
- 対象: tests/test_session.py, tests/test_hud.py (TC-092〜105) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `pytest -q tests/test_session.py tests/test_hud.py` -> 17 failed, 1 passed。失敗は全て AssertionError (ImportError/AttributeError なし)。passed の1件は TC-095 の CLEAR + 入力なし (「元のまま」) でスタブでも成立する。
  - `trace_check.py --stage tests` -> NG は TC-106 以降のみ (対象 TC-092〜105 は全て対応済み)。
  - 弱アサーション grep: `assert session.level is not None` のみ該当。型の絞り込み用ガードで、検証本体は別のアサーション。
  - 非決定性 grep: 該当なし。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| TEST-R-001 | new | Should | tests/test_session.py:124-135 (TC-099) | 仕様の前提「右入力 5 回でプレイヤーが x=37 に動く」を検証していない。右入力で動かない実装だと、死亡時に位置を戻さない実装でも (34,208) になり通る。 | カメラ変更前に box.x == 37 を確認する。 |
| TEST-R-002 | new | Should | tests/test_session.py:35-43,139-146 (TC-100) | 仕様の前提「敵は歩いて動いていた」を確認していない。敵が動かない実装だと、敵を復元しない実装でも (160,208,16,16) で通る。 | ヘルパー内で敵の box.x が 160 でないことを確認する。 |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 17 件全て AssertionError。 |
| TC 対応 | ✅ | TC-092〜105 に `# TC-NNN` あり。仕様外のテストなし。TC-104/105 は 1 つの parametrize にまとめている。 |
| 仕様一致 | ✅ | 期待値は仕様と一致 (34,208 / 3,0,0 / 600 / 160,208,16,16 / LIFE 2 など)。 |
| アサーションの強さ | ✅ | 具体値のタプル比較。TC-103 は 5 回分の screen 列を比較。 |
| 期待値の独立 | ✅ | 定数の再利用なし。 |
| 決定性・独立性 | ✅ | pygame・時間・乱数・ファイルなし。状態は関数ローカル。 |
| 実装非依存 | ✅ | 公開属性のみ。 |
| 境界値 | ✅ | TC-095 は 2x2、TC-098 は 3→2 と 2→1、TC-102 は lives=1。 |
| 構造 | ✅ | Given/When/Then を空行で分けている。 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装 (Green) 後の挙動 | 実装は未着手 (スタブ) | なし |

注記: スタブ (src/game/session.py) は box.x += 999、lives -= 1、CLEAR への遷移など中立でない値を返し、失敗の出方を歪めている。ただし本レビューの対象外で、全て AssertionError で落ちており判定には影響しない。

## 良い点
- 各テストが 1 つの振る舞いに絞られており、命名も振る舞いを表している。
- 期待値が手計算の具体値になっている。

# 基本設計レビュー結果
- 対象: docs/design/basic-design.md / 上流: docs/requirements/requirements.md / 回: 2（前回: basic-design-review-1.md）
- 判定: APPROVE
- 実行したコマンド: 検証コマンド3本。設計に未割当の REQ は無し、存在しない REQ への参照も無し。pygame の出現は render 層（DES-014/016/017）、§4 の draw シグネチャ、§7 判断12 のみ。JUMP_SPEED 345 / GRAVITY 900 / dt 1/60 の速度先更新で最高到達点 63.25 px を再計算し、REQ-006（62〜66 px）の範囲内であることを確認。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| DES-R-001 | resolved | Must | §5 #7 / §4 resolve_player_enemies / §7 判断8 | 踏んだ時にプレイヤー下端を敵上面へ合わせて重なりを解消し、その後 vy=-STOMP_BOUNCE_SPEED にすると明記された。辺が接するだけは overlaps=False（§4 Aabb）なので、次フレームの再接触による蹴り出しは起きない。 | - |
| DES-R-002 | resolved | Should | §4 resolve_shells_vs_walkers / resolve_player_enemies | 両関数の docstring に「alive=False の敵は無視する」が追記された。 | - |
| DES-R-003 | resolved | Should | §2 HeldButtons / §5 #1 | prev_jump_held の持ち主は main。複数ステップ時は jump_pressed を最初のステップだけ true にすると明記された。 | - |
| DES-R-004 | resolved | Should | §4 GameSession.update / §5 #11 | TITLE→PLAYING で lives/coins/score を初期化すると明記された。 | - |
| DES-R-005 | resolved | Should | §1 と §3 | 全 REQ について割当表と §3 の対応 REQ 列を突き合わせ、一致を確認した。DES-003 は「-」と明記された。 | - |
| DES-R-006 | resolved | Should | §4 update_enemy / next_camera_x | 式や処理順の記述が責務と制約の説明に改まった。 | - |

## 確認した観点
| 観点 | 結果(✅/❌/—) | 根拠 |
|---|---|---|
| 要件カバー | ✅ | comm の結果が両方空。割当表と §3 が双方向で一致。 |
| 層の分離 | ✅ | game 側のモジュールに pygame・実時間・ファイルの記述が無い。読込は main。 |
| 依存方向 | ✅ | main→render→game の一方向。循環なし。 |
| テスト容易性 | ✅ | dt、InputState、乱数なし。 |
| 状態の持ち主 | ✅ | prev_jump_held は main、coins/score/lives は Session、on_ground は Body のみ。 |
| インターフェース | ✅ | シグネチャ・単位・副作用あり。 |
| 更新順序 | ✅ | #3 のプレイヤー更新 → #4 ブロック → #5 敵 → #6/#7 接触 → #9 判定 → #10 カメラ → #11 Session の順に矛盾なし。slide_age は #5 で加算し #7 で蹴り出して 0 から始まるので、REQ-024/049 の境界（12 以内は無害）と整合。 |
| 定数表 | ✅ | 値・単位・出典あり。#11 の「+100/枚」は COIN_SCORE と同値で、定数表に載っている。 |
| 設計判断 | ✅ | 代替案と理由あり。 |
| 実現性 | ✅ | pygame-ce / pygbag 前提に問題なし。Python 3.14 との互換は §8 にリスクとして記載済み。 |
| スコープ | ✅ | 要件外の機能なし。 |
| 詳細度 | ✅ | 疑似コードなし。 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| pygbag と Python 3.14 の互換 | 実機確認は工程外。§8 に記載済み | なし |

## 良い点
- 前回の Must（連続接触）を、状態を増やさず押し上げで解消している。
- 判断の理由に数値の根拠（1 フレーム 4 px、最高到達点）がある。

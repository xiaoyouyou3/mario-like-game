# STATE（外部記憶: セッションをまたいだ現在地）

更新ルール: 工程の開始・完了・承認・差戻しのたびに、親が必ず更新する。

| 項目 | 値 |
|---|---|
| 現在の工程 | 5. 完了確認（完了。残りは Git の初期化・プッシュと、人間による手動確認 MC-001〜012） |
| 状態 | 全30グループ Green・レビュー APPROVE。render/main/stage1/素材/pygbag ビルドは作成済み。追加テストも APPROVE。残り: Git 初期化・リモート作成・プッシュ、人間による手動確認 |
| 次のアクション | stage1.txt → 素材とASSETS.md → renderer.draw → main.py → 工程5（完了確認）→ git |

## 承認ログ
| 成果物 | 人間の承認 | 日付 |
|---|---|---|
| 要件定義書 | 済（未決事項 #1〜6 に回答、REQ-050 追加、REQ-103/104 の検証環境を確定。REQ-051 は変更要求として人間が指示、要件レビュー3回目 APPROVE） | 2026-11-03 |
| 基本設計書 | 済（人間の指示「REQ-051 反映後にレビューを通過したら進める」。基本設計レビュー3回目 APPROVE で確定） | 2026-11-03 |

## レビュー履歴
| 工程 | 往復 | 判定 | レビューファイル | 未解決 Must |
|---|---|---|---|---|
| 1. 要件定義 | 1 | REJECT | docs/reviews/requirements-review-1.md | REQ-R-001（2回目で解消） |
| 1. 要件定義 | 2 | APPROVE | docs/reviews/requirements-review-2.md | なし（Should 2件: 優先度の偏り、REQ-049 の表外→表内に修正済み） |
| 2. 基本設計 | 1 | REJECT | docs/reviews/basic-design-review-1.md | DES-R-001（2回目で解消） |
| 2. 基本設計 | 2 | APPROVE | docs/reviews/basic-design-review-2.md | なし（Should 0件） |
| 変更要求 REQ-051 | 要件3 / 設計3 | APPROVE / APPROVE | docs/reviews/requirements-review-3.md, basic-design-review-3.md | なし（要件 Should 2件: 優先度の偏り、REQ-051 の並び順） |
| 3. テスト仕様 | 1 | REJECT | docs/reviews/test-spec-review-1.md | SPEC-R-001〜003（2回目で解消） |
| 3. テスト仕様 | 2 | APPROVE | docs/reviews/test-spec-review-2.md | なし（Should 1件: TC-083 備考の数値→修正済み） |
| 4d G06〜G09 実装 | 1 | APPROVE | docs/reviews/code-review-batch04.md | なし |
| 4d G10〜G12 実装 | 1 | APPROVE | docs/reviews/code-review-batch05.md | なし（Should CODE-R-001: PLAYER_W/H を constants へ移動済み） |
| 4d G13〜G15 実装 | 1 | APPROVE | docs/reviews/code-review-batch06.md | なし |
| 4d G16〜G18 実装 | 1 | APPROVE | docs/reviews/code-review-batch07.md | なし |
| 4d G19 実装 | 1 | APPROVE | docs/reviews/code-review-batch08.md | なし |
| 4d G20〜G22b 実装 | 1 | APPROVE | docs/reviews/code-review-batch09.md | なし |
| 4d G23〜G25 実装 | 1 | APPROVE | docs/reviews/code-review-batch10.md | なし |
| 4d G26〜G27 実装 | 1 | APPROVE | docs/reviews/code-review-batch11.md | なし |
| 4a 追加 TC-115/117/118 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch12.md | - |
| 4a G26〜G27 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch11.md | なし |
| 4a G23〜G25 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch10.md | なし（Should TEST-R-001/002: 前提の検証を追加済み） |
| 4a G20〜G22b テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch09.md | なし |
| 4a G19 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch08.md | なし |
| 4a G16〜G18 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch07.md | なし |
| 4a G13〜G15 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch06.md | なし |
| 4a G10〜G12 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch05.md | なし |
| 4a G06〜G09 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch04.md | なし |
| 4a G05 テストコード | 1 | APPROVE | docs/reviews/test-code-review-batch03.md | なし |
| 4d G05 実装 | 1 | APPROVE | docs/reviews/code-review-batch03.md | なし |
| 4d G03+G04 実装 | 1 | APPROVE | docs/reviews/code-review-batch02.md | なし |
| 4a G03+G04 テストコード | 1 | REJECT | docs/reviews/test-code-review-batch02.md | TEST-R-001（修正済み・再レビューで確認） |

## TDD サイクル進捗
| TC グループ | Red | Green | Refactor | レビュー | コミット |
|---|---|---|---|---|---|
| G01 入力状態 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G02 幾何 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G27a 定数 (TC-112, 113) | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G03 ステージ解析 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G04 ステージ異常 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G05 タイルマップ | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G06 重力 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G07 移動と衝突 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G08 壁と天井 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G09 角・端・落下 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G10 水平移動 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G11 ダッシュと減速 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G12 ジャンプ | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G13 敵の基本 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G14 敵の反転 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G15 敵の状態遷移 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G16 踏みつけ | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G16b 踏みつけの結果 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G17 接触死亡 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G18 甲羅 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G19 カメラ | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G20 Level 基本 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G21 Level ブロック | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G22 Level 判定 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G22b Level 判定の補足 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G23 Session 画面 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G24 Session プレイ | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G25 Session 終了 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G26 描画の純粋部分 | 済 | 済 | 済 | APPROVE（test-code / code） | - |
| G27 倍率 (TC-111) | 済 | 済 | 済 | APPROVE（test-code / code） | - |

## 未決事項 / 人間への質問
- なし

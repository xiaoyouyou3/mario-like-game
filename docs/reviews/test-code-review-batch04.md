# テストコードレビュー結果
- 対象: tests/test_physics.py (TC-022〜035) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `pytest -q tests/test_physics.py`: 22 failed, 2 passed。失敗は全て assert の比較失敗。AttributeError/TypeError/ImportError/NameError は 0 件
  - `trace_check.py --stage tests`: TC-022〜035 に関する NG なし（NG は他バッチの TC のみ）
  - 弱いアサーション・非決定性の grep: 該当なし

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | スタブ（apply_gravity は pass、move_and_collide は x に vx を足すだけ）に対し AssertionError で失敗。通った 2 件は TC-023 の vy=240 と TC-029 の (148, 0) で、スタブの中立値と境界の期待値が一致しただけ。parametrize の他の点が落ちている |
| TC 対応 | ✅ | TC-022〜035 の 14 件に `# TC-NNN` あり。仕様書にない TC なし |
| 仕様一致 | ✅ | 入力・期待値を仕様書の行と照合し、全件一致 |
| アサーションの強さ | ✅ | 手計算の具体値と pytest.approx。TC-035 は max==240 で上限超過も検出 |
| 期待値の独立 | ✅ | 定数の再利用なし |
| 決定性・独立性 | ✅ | pygame/時間/乱数/ファイルなし。共有状態なし（TC-035 の tilemap もテスト内ローカル） |
| 境界値 | ✅ | TC-022/023/029/031/032/034 が 3 点または仕様どおりの点を parametrize |
| 構造と命名 | ✅ | Given/When/Then が空行で分離、名前が振る舞いを表す |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 実装での Green | レビュー対象外 | なし |

## 良い点
- 境界ちょうど（接触は衝突なし）を TC-029/031 で検証している
- 期待値が手計算の具体値で書かれている

# テストコードレビュー結果
- 対象: tests/test_render_pure.py (TC-106〜111), tests/test_constants.py (TC-112/113) / 上流: docs/test-specs/test-spec.md, docs/design/basic-design.md / 回: 1
- 判定: APPROVE
- 実行したコマンド:
  - `pytest -q tests/test_render_pure.py`: 21 failed, 2 passed。失敗は全て値の不一致の AssertionError（compute_scale が 0、HeldButtons の各項目の不一致など）。ImportError/AttributeError はない。
  - 通った 2 件は TC-108 の (b) と (e)。期待値が「すべて偽」で、スタブの戻り値と一致するため。仕様どおりの中立ケースで問題なし。
  - `pytest -q tests/test_constants.py`: 2 passed（TC-112/113 は定数実装済みで最初から緑。既存テストのため対象外）。
  - `trace_check.py --stage tests`: 欠落は TC-115/117/118 のみ（本バッチ対象外）。TC-106〜113 は対応済み。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| 有効な Red | ✅ | 全て AssertionError |
| TC 対応 | ✅ | TC-106〜111 に `# TC-NNN` あり。TC-112/113 は test_constants.py にある |
| 仕様一致 | ✅ | TC-108 の座標・レイアウトは仕様どおり。TC-111 の 7 点も一致 |
| アサーションの強さ | ✅ | HeldButtons 全項目の等価比較。境界は辺の含む/含まないを検証。TC-106 は収まりと重なりを両方見る |
| 期待値の独立 | ✅ | 期待値は直書き。TC-107/109 の中心座標は、レイアウトと変換が矛盾しないことを見るため適切 |
| 決定性・独立性 | ✅ | ウィンドウ生成なし。pygame は定数のみ使用。共有可変状態なし |
| 実装非依存 | ✅ | 公開関数のみ使用 |
| 境界値 | ✅ | TC-108 と TC-111 が仕様どおり複数点を検証 |
| 構造と命名 | ✅ | Given/When/Then が分かれ、名前が振る舞いを表す |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| TC-115/117/118 | 本バッチ対象外 | なし |

## 良い点
- 境界値を parametrize で網羅し、スタブとの偶然一致も中立ケースに限られている。

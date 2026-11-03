# コードレビュー結果 (batch11 render 純粋部分)
- 対象: src/render/touch_controls.py, src/render/input_mapper.py, src/render/renderer.py / 上流: docs/test-specs/test-spec.md (TC-106〜111), docs/design/basic-design.md (DES-014〜016), docs/requirements/requirements.md / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q = 223 passed / ruff = All checks passed / grep pygame src/game = 0件 / 危険API grep (src) = 0件

## 指摘
なし

## 確認した観点
| 観点 | 結果(✅/❌/—) | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 直書き・テスト専用分岐なし。compute_scale は max(1, min(w//SCREEN_W, h//SCREEN_H)) の一般式 |
| 仕様適合 | ✅ | TC-108 の境界（左・上を含み右・下を含まない）が `<=` / `<` で実装。TC-109 のキー割当（←→/Z/X）と default_layout の対応が一致。TC-110 は emscripten 以外で False |
| 過剰実装 | ✅ | 仕様外の機能なし |
| 層の分離 | ✅ | src/game に pygame なし。render は game を import のみ。ルール判断なし |
| 設計一致 | ✅ | DES-014/015/016 の責務・依存と一致。HeldButtons を作るだけで jump 履歴は持たない（main の責務） |
| 定数 | ✅ | SCREEN_W/H は constants.py から参照。ボタン座標はレイアウト定義そのもの |
| 入力検証・危険API | ✅ | 該当なし |
| 数値の頑健性 | ✅ | 整数除算のみ。0 サイズ窓でも max(1, ...) で 1 |
| 型・構造 | ✅ | 型ヒントあり、関数は短い |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| ブラウザ上の detect_touch_device 分岐 | 自動テスト対象外（手動確認 REQ-103/104） | なし |
| renderer.py の Session 描画 (DES-016 の残り) | 現時点で未実装（compute_scale のみ）。本バッチ範囲外と判断 | なし |

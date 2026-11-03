# コードレビュー結果
- 対象: src/game/physics.py, src/game/constants.py / 上流: docs/test-specs/test-spec.md (TC-022〜035), docs/design/basic-design.md (DES-006) / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q (68 passed), ruff check . (All checks passed), grep pygame/time/random in src/game (0件), 数値リテラル候補 grep (physics.py に該当なし)

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| (なし) | | | | | |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 値の直書き・テスト専用分岐なし。一般式 |
| 仕様適合 | ✅ | GRAVITY=900, FALL_MAX_SPEED=240 は TC-022/023 の備考と一致。x→y の順で解決 (TC-033) |
| 過剰実装 | ✅ | 仕様外の引数・分岐なし |
| 層の分離 | ✅ | pygame・実時間・乱数なし |
| 設計一致 | ✅ | DES-006 の依存 (constants, geometry, tilemap) のみ |
| 定数 | ✅ | physics.py に直書きなし。単位コメントあり |
| 数値の頑健性 | ✅ | tile_span は floor/ceil で負座標も安全。左右端は is_solid が壁扱い。固定 dt では最大落下 4px/フレームでタイル幅未満 |
| 型・構造 | ✅ | 型ヒントあり、全関数 50 行以内 |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| 大きな dt でのすり抜け | 仕様は固定 dt (REQ-101)。dt 上限の要求なし | なし |

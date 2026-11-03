# コードレビュー結果
- 対象: src/game/interactions.py（関連: src/game/constants.py, src/game/enemy.py）/ 上流: docs/test-specs/test-spec.md (TC-063〜077, TC-119), docs/design/basic-design.md (DES-009) / 回: 1
- 判定: APPROVE
- 実行したコマンド: pytest -q は 152 passed。ruff check は All checks passed。pygame、実時間、グローバル乱数、危険API の grep はいずれも 0 件。interactions.py 内のマジックナンバー候補の grep は 0 件。git は無いため差分規模は未確認。

## 指摘
| ID | 状態 | 重大度 | 場所 | 問題と失敗シナリオ | 修正案 |
|---|---|---|---|---|---|
| なし | - | - | - | - | - |

## 確認した観点
| 観点 | 結果 | 根拠 |
|---|---|---|
| テスト迎合 | ✅ | 直書きや専用分岐はなく、STOMP_ZONE_RATIO を使う一般式になっている |
| 仕様適合 | ✅ | 踏みつけ境界 216 は top+h*0.5。猶予は slide_age > 12。バウンスは -200。TC-063〜077・119 に対応するテストがある |
| 過剰実装 | ✅ | 仕様外の分岐はない |
| 層の分離 | ✅ | 純Python。依存は constants, enemy, player のみ |
| 設計一致 | ✅ | DES-009 の責務と一致。状態は Enemy/Player が持ち、ここでは複製しない |
| 定数 | ✅ | すべて constants.py に定義済み |
| 順序非依存 | ✅ | 踏みつけ集合を先に確定してから解決する。リスト順に依存しない（TC-072, 076） |
| 蹴った直後の死亡判定 | ✅ | kick_shell が slide_age=0 にするため猶予内で死亡しない |
| 数値の頑健性 | ✅ | 重なり判定のみで、除算や int 丸めはない |
| 型・構造 | ✅ | 型ヒントあり。関数は短い |

## 未確認範囲
| 項目 | 理由 | 判定への影響 |
|---|---|---|
| Level からの呼び出し順 | DES-011 の範囲で、この回の対象外 | なし |

## 良い点
- 踏みつけ対象を先に確定する構成で、リスト順に依存しない。

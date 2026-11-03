---
name: run-tests
description: pytest と ruff を実行し、結果を「有効なRed / Green / 失敗」に分類して報告し、TDD の証跡ログを更新する。Red確認・Green確認・コミット前・レビュー依頼前に使う。
---

# テスト実施

## 実行コマンド
| 目的 | コマンド |
|---|---|
| 対象のみ | `.venv/bin/pytest -q tests/test_x.py::test_name` |
| 全体 | `.venv/bin/pytest -q` |
| Lint | `.venv/bin/ruff check .` |
| トレーサビリティ | `.venv/bin/python scripts/trace_check.py --stage tests` |

`.venv` がなければ `test-env` を先に実行する。pytest が exit code 5（テスト0件）なら「テストが収集されていない」として報告する。

## 判定（必ずこの分類で報告する）
| 状況 | 判定 | 次の行動 |
|---|---|---|
| 対象が `AssertionError` で失敗 | 有効な Red | 実装へ |
| 対象が ImportError / AttributeError / TypeError / SyntaxError / NameError / 収集エラー | 無効な Red（環境・構造） | test-code に戻る |
| 対象が最初から通る（Red のはず） | 無効な Red（テストが弱い） | テストを強化 |
| 対象も全体も通る、ruff OK | Green | リファクタ or 次へ |
| 対象は通るが既存テストが落ちた | 回帰 | 実装を直す（テストを緩めない） |

## 報告形式
```
判定: 有効なRed | 無効なRed(理由) | Green | 回帰
pytest: 通過 N / 失敗 M / エラー K （全体 T 件）
失敗したテスト: tests/test_player.py::test_x — assert 0.0 == approx(12.0)（期待 12.0, 実際 0.0）
ruff: OK | 件数
実行コマンド: <実際に実行したコマンド>
```

## 証跡ログ `docs/evidence/tdd-log.md`
1行1TCグループで追記・更新する。
```
| TCグループ | Red（日付 / 失敗の要点） | Green（変更ファイル / 全体件数） | Refactor |
```

## 禁止
- テストの削除・skip・期待値の緩和で緑にする。
- 実行せずに結果を推測で報告する。

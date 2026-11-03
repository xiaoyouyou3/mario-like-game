---
name: test-env
description: Python 仮想環境（.venv）の作成・検証・再構築を行う。初回セットアップ、依存追加後、「テストが動かない」「環境が壊れた」のときに使う。Docker が無い環境向け。
---

# テスト環境（venv）

## 構築と検証
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -c "import pygame, pytest; print(pygame.version.ver, pytest.__version__)"
.venv/bin/ruff --version
```
全て成功したら環境 OK。`pytest -q` が exit code 5（テスト0件）でも、環境としては正常。

## トラブル対応
| 症状 | 対処 |
|---|---|
| `No module named pygame` | venv ではなくシステムの python を使っている。`.venv/bin/python` を使う |
| pygame の wheel が無い | Python のバージョンを確認。`pygame-ce` を使う（`pygame` ではない） |
| ウィンドウが開けない環境 | ロジックのテストでは不要。必要なら `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy` |
| 依存を追加した | `requirements.txt` に追記して再インストール。バージョンは下限のみ固定 |

## 再構築
`rm -rf .venv` は環境の破棄なので、ユーザーに確認してから実行する。

## 将来（Docker が使える場合）
同じ手順を `Dockerfile` に移し、`docker run` で `pytest -q` を実行する構成に置き換える。

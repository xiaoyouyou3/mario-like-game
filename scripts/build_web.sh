#!/bin/sh
# Web 版(pygbag)ビルド。pygbag はフォルダ丸ごとを APK にするため、
# .venv や docs を含めないよう、必要なファイルだけを一時フォルダに集めてからビルドする。
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir "$TMP/mario-like-game"
cp -r "$ROOT/main.py" "$ROOT/src" "$ROOT/assets" "$TMP/mario-like-game/"
find "$TMP" -name __pycache__ -prune -exec rm -rf {} +
"$ROOT/.venv/bin/pygbag" --build "$TMP/mario-like-game"
rm -rf "$ROOT/build"
mkdir -p "$ROOT/build"
cp -r "$TMP/mario-like-game/build/web" "$ROOT/build/web"
ls -la "$ROOT/build/web"

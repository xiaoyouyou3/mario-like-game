# 素材一覧（REQ-047）

ゲームが使う画像は、すべてこのリポジトリの `scripts/make_assets.py` が生成するドット絵で、第三者の素材は含まない。

| ファイル | 内容 | 出所 | ライセンス |
|---|---|---|---|
| assets/images/player.png | プレイヤー 12x16 | scripts/make_assets.py（自作） | CC0 1.0（本プロジェクトの作者が提供） |
| assets/images/walker.png | 歩く敵 16x16 | 同上 | 同上 |
| assets/images/koopa.png | 甲羅の敵（歩行） 16x16 | 同上 | 同上 |
| assets/images/shell.png | 甲羅（静止・滑走） 16x16 | 同上 | 同上 |
| assets/images/solid.png | 壁・地面タイル 16x16 | 同上 | 同上 |
| assets/images/question.png | ? ブロック 16x16 | 同上 | 同上 |
| assets/images/used.png | 使用済みブロック 16x16 | 同上 | 同上 |
| assets/images/flag.png | 旗 16x16 | 同上 | 同上 |

再生成: `.venv/bin/python scripts/make_assets.py`

## 要確認
「自作の素材を CC0 として扱う」ことは、プロジェクトの作者（人間）の判断を要する。別の CC0 素材（例: OpenGameArt の CC0 ライセンスのもの）へ差し替える場合は、このファイルに入手元 URL とライセンスを追記する。

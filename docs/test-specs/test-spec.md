# テスト仕様書

最終更新: 2026-11-13（変更要求 2 件目: 穴を画面の下端まで通す。TC-129〜131, MC-015 を追加し MC-013 を変更。変更要求 1 件目: 画面サイズ・操作パネル。TC-080, 106, 111, 113, 116 を変更し TC-123〜128, MC-013, 014 を追加）/ 対応: docs/requirements/requirements.md（REQ-001〜058, 101〜105）, docs/design/basic-design.md（DES-001〜019）

## 0. 共通の前提
| 項目 | 内容 |
|---|---|
| dt | 特に書かない限り 1/60 秒。浮動小数の比較は `pytest.approx` |
| テスト用ステージ | 200x15 の全マスが `.` の文字列から、指定したマスだけ置き換えて作る補助関数 `stage_text(cells, start=(2,13), flag=((198,12),))`（tests/conftest.py）。`start` と `flag` は既定で `P` と `F` を置く（`parse_stage` が `P` と `F` を必須とするため）。TC が `P` や `F` のマスを指定したときは、その指定を使う（既定は置かない）。`start=None` / `flag=None` で置かない。既定の旗は x 3168〜3184 で、他の TC の位置から十分離れている。`parse_stage` に渡し、TileMap / Level / Session に使う |
| 接地済みの Level / Session | `Level(data)` は生成直後のプレイヤーの `on_ground` が偽。ジャンプを検証する TC は、生成後（Session は TITLE→PLAYING の後）に入力なしで `step` / `update` を 1 回進めて接地させてから始める |
| 水平移動の規則 | 入力方向 d は 左=-1, 右=+1, 左右同時または入力なし=0。最大速度 max は run が真なら 150、偽なら 90。減速度 DECEL は接地中 900、空中 360。加速度 ACCEL は接地・空中とも 720。(1) d≠0 かつ vx が d と逆向き、または d の向きで abs(vx) ≤ max: vx を d の向きに ACCEL*dt だけ変え、±max に収める。(2) d≠0 で d の向きに abs(vx) > max: DECEL*dt だけ減らし、max を下回らない。(3) d=0: abs(vx) を DECEL*dt だけ減らし、0 を下回らない |
| 敵の更新規則 | 崖の判定は「足元の判定位置が固体か」を調べる。判定位置は 進行方向の端の外へ 1 px、下へ 1 px（右向きは 右端+1、左向きは 左端-1）。崖の反転は 判定→反転→移動 の順。壁の反転は 移動→衝突解決→反転 の順。崖の判定は WALKING の接地中だけ行う。ステージ下端より下（上端 > 240）に落ちた敵は取り除く |
| 地面 | 「地面あり」は row 14 の col 0〜199 がすべて `#`（床の上面 y = 224）。「地面なし」は row 14 も `.` |
| 座標 | 左上原点。タイル (col, row) の左上は (16*col, 16*row) |
| 地上プレイヤー | `create_player(x, 208.0)` を作り、`body.on_ground = True` にしたもの。幅 12・高さ 16 |
| 地上の敵 | `create_enemy(kind, x, 208.0)` を作り、`body.on_ground = True` にしたもの。幅 16・高さ 16 |
| 甲羅の設定 | 滑走する甲羅は KOOPA に `state = SHELL_SLIDING`・`direction = ±1` を直接設定して作る。静止甲羅は `state = SHELL_IDLE` |
| 敵の初期方向 | `create_enemy` は左向き（direction = -1）で作る |
| 配置規則 | ステージの `P` はタイルの下端にプレイヤーの下端を合わせ、タイルの中央に置く（x = 16*col + 2, y = 16*row）。`W` `K` はタイルと同じ位置（x = 16*col, y = 16*row） |
| ステージ定数 | 幅 3200 px、高さ 240 px。踏みつけの許容は敵の上半分（敵の上面 + 8 px） |
| 異常系メッセージ | `StageFormatError` のメッセージは、幅不正は `width`、高さ不正は `height`、未知の文字は `unknown character`、開始位置は `start`、旗は `flag` を含む |

## 1. 自動テストケース
種別: 正常 / 境界 / 異常 / 状態遷移 / 回帰

| ID | グループ | 対応 REQ / DES | 前提 (Given) | 操作 (When) | 期待結果 (Then) | 種別 | 備考(計算根拠) |
|---|---|---|---|---|---|---|---|
| TC-001 | G01 入力状態 | REQ-045 / DES-002 | `HeldButtons(jump=j)` と前回の jump 押下状態 prev | `make_input(held, prev)` を (j, prev) = (真, 偽), (真, 真), (偽, 真), (偽, 偽) で呼ぶ | `jump_pressed` がそれぞれ 真, 偽, 偽, 偽 | 状態遷移 | 押した瞬間だけ真 |
| TC-002 | G01 入力状態 | REQ-045 / DES-002 | `HeldButtons(left, right, jump, run)` の各項目を 1 つずつ真にしたもの | `make_input(held, False)` | `left` `right` `run` が `held` の同名の項目と同じ値になる | 正常 | 4 通りを parametrize |
| TC-003 | G01 入力状態 | REQ-045 / DES-002 | a = (left のみ真), b = (right と jump が真) | `merge_held(a, b)` | left, right, jump が真で run が偽 | 正常 | 項目ごとの OR |
| TC-004 | G02 幾何 | - / DES-003 | `Aabb(10, 20, 30, 40)` | `left` `right` `top` `bottom` `center_x` を読む | 10, 40, 20, 60, 25 | 正常 | right=10+30, bottom=20+40, center_x=10+15 |
| TC-005 | G02 幾何 | - / DES-003 | a = `Aabb(0,0,16,16)` | b = (8,8,16,16) / (15,0,16,16) / (16,0,16,16) / (0,16,16,16) / (40,40,16,16) との `a.overlaps(b)` | 真, 真, 偽, 偽, 偽 | 境界 | 辺が接するだけ（x=16, y=16）は偽 |
| TC-006 | G02 幾何 | REQ-008 / DES-003 | なし | `tile_span(lo, hi)` を (0,16), (0,16.5), (16,32), (-1,1), (15.9,16.1) で呼ぶ | `range(0,1)`, `range(0,2)`, `range(1,2)`, `range(-1,1)`, `range(0,2)` | 境界 | floor(lo) から ceil(hi)-1 まで。負でも floor |
| TC-007 | G03 ステージ解析 | REQ-042 / DES-004 | `#` を (3,14)、`?` を (5,10)、`.` を (6,14) に置き、`P` を (2,13)、`F` を (9,10) に置いたステージ文字列 | `parse_stage(text)` | `tiles[14][3]` が SOLID、`tiles[10][5]` が QUESTION、`tiles[14][6]` が EMPTY | 正常 | `P` `F` のマスは EMPTY |
| TC-008 | G03 ステージ解析 | REQ-042 / DES-004 | `P` を (2,13) に置いたステージ | `parse_stage(text)` | `start == (2, 13)` | 正常 | |
| TC-009 | G03 ステージ解析 | REQ-042 / DES-004 | `W` を (10,13) と (20,13)、`K` を (30,13) に置いたステージ | `parse_stage(text)` | `walkers == ((10,13),(20,13))`、`koopas == ((30,13),)` | 正常 | 読み順は上の行から、左から |
| TC-010 | G03 ステージ解析 | REQ-042 / DES-004 | `F` を (198,10), (198,11), (198,12) に置いたステージ | `parse_stage(text)` | `flag == Aabb(3168, 160, 16, 48)` | 正常 | x=198*16=3168, y=10*16=160, 高さ=3*16 |
| TC-011 | G03 ステージ解析 | REQ-043 / DES-004 | 200 文字 x 15 行の有効なステージ | `parse_stage(text)` | `len(tiles)` が 15、`len(tiles[0])` が 200（高さ 240 px・幅 3200 px） | 境界 | 15*16=240, 200*16=3200 |
| TC-012 | G04 ステージ異常 | REQ-043 / DES-004 | 3 行目だけ 199 文字のステージ | `parse_stage(text)` | `StageFormatError`（`match="width"`） | 異常 | |
| TC-013 | G04 ステージ異常 | REQ-043 / DES-004 | 14 行のステージ（または 16 行） | `parse_stage(text)` | `StageFormatError`（`match="height"`） | 異常 | 14 と 16 を parametrize |
| TC-014 | G04 ステージ異常 | REQ-042 / DES-004 | (4,4) に `X` を置いたステージ | `parse_stage(text)` | `StageFormatError`（`match="unknown character"`） | 異常 | |
| TC-015 | G04 ステージ異常 | REQ-042 / DES-004 | `P` がないステージ、または `P` が 2 つのステージ | `parse_stage(text)` | `StageFormatError`（`match="start"`） | 異常 | 0 個と 2 個を parametrize |
| TC-016 | G04 ステージ異常 | REQ-042 / DES-004 | `F` がないステージ | `parse_stage(text)` | `StageFormatError`（`match="flag"`） | 異常 | |
| TC-017 | G05 タイルマップ | REQ-009 / DES-005 | (1,1) が EMPTY、(2,1) が SOLID、(3,1) が QUESTION のタイルマップ。(3,1) を叩いて USED にしたものも用意する | `is_solid(col, 1)` | EMPTY は偽、SOLID・QUESTION・USED は真 | 正常 | |
| TC-018 | G05 タイルマップ | REQ-009 / DES-005 | 200x15 のタイルマップ | `is_solid` を (-1,5), (200,5), (0,-1), (0,15) で呼ぶ | 真, 真, 偽, 偽 | 境界 | 左右端は壁、上端の外と下端の外は空 |
| TC-019 | G05 タイルマップ | REQ-026 / DES-005 | (3,1) が QUESTION のタイルマップ | `hit_question(3, 1)` の後に `tile_at(3, 1)` | 戻り値が真、`tile_at` が USED | 正常 | |
| TC-020 | G05 タイルマップ | REQ-027 / DES-005 | (3,1) が USED、(2,1) が SOLID、(1,1) が EMPTY のタイルマップ | `hit_question` を (3,1), (2,1), (1,1) に呼ぶ | すべて戻り値が偽で、`tile_at` は USED, SOLID, EMPTY のまま | 異常 | |
| TC-021 | G05 タイルマップ | REQ-048 / DES-005 | 同じ `StageData` から作った TileMap を 1 つ叩いて USED にしたもの | 同じ `StageData` から新しい TileMap を作り、同じマスの `tile_at` を読む | 新しい方は QUESTION のまま。`StageData.tiles` も QUESTION のまま | 回帰 | StageData は不変 |
| TC-022 | G06 重力 | REQ-006 / DES-006 | `Body` の vy が 0, -345, 100 | `apply_gravity(body, 1/60)` | vy が 15, -330, 115 | 正常 | 900*(1/60)=15 |
| TC-023 | G06 重力 | REQ-007 / DES-006 | `Body` の vy が 224, 225, 240 | `apply_gravity(body, 1/60)` | vy が 239, 240, 240 | 境界 | 224+15=239、225+15=240 に頭打ち、240+15=255 は 240 |
| TC-024 | G07 移動と衝突 | REQ-001 / DES-006 | 何もない空間の `Body(Aabb(100,100,12,16), vx=60, vy=0)` | `move_and_collide(body, tilemap, 1/60)` | x == 101、y == 100、`on_ground` が偽、`CollisionResult` のすべてが偽、vx は 60 のまま | 正常 | 60*(1/60)=1 |
| TC-025 | G07 移動と衝突 | REQ-009 / DES-006 | `Body(Aabb(100,100,12,16), vx=60, vy=120)` | dt=0 で `move_and_collide` | 位置が (100, 100) のまま | 境界 | |
| TC-026 | G07 移動と衝突 | REQ-008 / DES-006 | 地面あり。`Body(Aabb(100,207,12,16), vx=0, vy=120)` | `move_and_collide(body, tilemap, 1/60)` | y == 208、vy == 0、`on_ground` が真 | 正常 | 207+2=209、下端 225 が床の上面 224 を超えるので y=224-16=208 |
| TC-027 | G07 移動と衝突 | REQ-008 / DES-006 | 地面あり。`Body(Aabb(100,208,12,16), vy=15, on_ground=True)` | `move_and_collide` | y == 208、vy == 0、`on_ground` が真 | 正常 | 接地中は毎フレーム再計算される |
| TC-028 | G07 移動と衝突 | REQ-011 / DES-006 | row 14 の col 0〜5 だけ床。`Body(Aabb(100,208,12,16), vy=15, on_ground=True)` | `move_and_collide` | y == 208.25、vy == 15、`on_ground` が偽 | 正常 | x=100 は床の右端 96 より外。15*(1/60)=0.25 |
| TC-029 | G08 壁と天井 | REQ-009 / DES-006 | col 10 の row 12・13 が壁（x 160〜176）。`Body` の (x, vx) = (147, 120), (148, 0), (148, 60)、y=200 | `move_and_collide` | (x, vx, hit_right) が (148, 0, 真), (148, 0, 偽), (148, 0, 真) | 境界 | 147+2=149 で右端 161。壁の左 160-12=148。ぴったり接している状態は衝突なし |
| TC-030 | G08 壁と天井 | REQ-009 / DES-006 | col 5 の row 12・13 が壁（x 80〜96）。`Body(Aabb(96.5,200,12,16), vx=-60)` | `move_and_collide` | x == 96、vx == 0、`hit_left` が真 | 正常 | 96.5-1=95.5 で壁に入る。壁の右端 96 に戻す |
| TC-031 | G08 壁と天井 | REQ-010 / DES-006 | col 6 の row 8 が固体（x 96〜112、y 128〜144）。`Body` の (x, y) = (98, 144.5) と (112, 144.5)、vy=-60 | `move_and_collide` | (y, vy, hit_ceiling, ceiling_cell) が (144, 0, 真, (6,8)) と (143.5, -60, 偽, None) | 境界 | 144.5-1=143.5 で天井に入る。x=112 は固体の右端に接するだけ |
| TC-032 | G08 壁と天井 | REQ-010 / DES-006 | col 5 と col 6 の row 8 が固体。`Body` の x が 89, 90, 91、y=144.5、vy=-60 | `move_and_collide` | `ceiling_cell` が (5,8), (5,8), (6,8) | 境界 | 中心 x=95 は col 5 の中心 88 に 7、col 6 の中心 104 に 9。x=90 は中心 96 で 8 と 8 の同距離のため、列番号の小さい方。x=91 は中心 97 で 9 と 7 |
| TC-033 | G09 角・端・落下 | REQ-008 / DES-006 | 地面あり、col 10 の row 12・13 が壁。`Body(Aabb(147,207,12,16), vx=120, vy=120)` | `move_and_collide` | x == 148、y == 208、vx == 0、vy == 0、`on_ground` が真、`hit_right` が真 | 境界 | x を先に解決し、その後 y を解決する。角で引っかからない |
| TC-034 | G09 角・端・落下 | REQ-009 / DES-006 | 200x15 のタイルマップ。`Body` の (x, vx) = (0.5, -60) と (3187.5, 60)、y=200 | `move_and_collide` | x が 0 と 3188、vx が 0、`hit_left` と `hit_right` が真 | 境界 | ステージの左右端は壁。3188+12=3200 |
| TC-035 | G09 角・端・落下 | REQ-007 / DES-006 | 地面なし。`Body(Aabb(100,0,12,16))` の vy=0 | `apply_gravity` と `move_and_collide` を 100 回繰り返す | 途中の vy の最大値が 240 で、240 を超えない | 境界 | 16 回目に 240 に達する |
| TC-036 | G10 水平移動 | REQ-001 / DES-007 | 地面あり。地上プレイヤー (x=50)、vx=0 | 右入力で `update_player` を 1 回 | vx == 12 | 正常 | 720*(1/60)=12 |
| TC-037 | G10 水平移動 | REQ-001 / DES-007 | 地面あり。地上プレイヤー。(初期 vx, 右入力の回数) = (0, 30), (84, 1), (90, 1) | `update_player` を指定回数 | vx が 90, 90, 90 | 境界 | 30 回で 0.5 秒。84+12=96 は 90 に頭打ち |
| TC-038 | G10 水平移動 | REQ-001 / DES-007 | 地面あり。地上プレイヤー、vx=0 | 左入力で 1 回 | vx == -12 | 正常 | 符号が逆 |
| TC-039 | G10 水平移動 | REQ-001 / DES-007 | 地面あり。地上プレイヤーの vx が 0 と 60 | 左と右の入力を同時に 1 回 | vx が 0 と 45 | 異常 | 入力なしと同じ扱い。60-900*(1/60)=45 |
| TC-040 | G10 水平移動 | REQ-001 / DES-007 | 地面あり。地上プレイヤー、vx=60 | 左入力で 1 回 | vx == 48 | 境界 | 反対向きの入力も加速度で働く。60-12=48 |
| TC-041 | G11 ダッシュと減速 | REQ-002 / DES-007 | 地面あり。地上プレイヤー、vx=0 | run と右入力で 60 回 | vx == 150 | 境界 | 1.0 秒。12 ずつ増えて 150 で頭打ち |
| TC-042 | G11 ダッシュと減速 | REQ-003 / DES-007 | 地面あり。地上プレイヤー、vx=90 | 入力なしで 1 回 | vx == 75 | 正常 | 90-900*(1/60)=75 |
| TC-043 | G11 ダッシュと減速 | REQ-003 / DES-007 | 地面あり。地上プレイヤー、vx=90 | 入力なしで 5, 6, 7 回 | vx が 15, 0, 0 | 境界 | 90-15*5=15、6 回で 0、負にならない |
| TC-044 | G11 ダッシュと減速 | REQ-003 / DES-007 | 地面あり。地上プレイヤー、vx=0 | 右入力で 30 回、続けて入力なしで 30 回 | vx == 0 | 正常 | 要件の受入条件そのまま |
| TC-045 | G11 ダッシュと減速 | REQ-003 / DES-007 | 地面なし。空中のプレイヤー (y=100)、vx=90 | 入力なしで 1 回 | vx == 84 | 正常 | 90-360*(1/60)=84 |
| TC-046 | G12 ジャンプ | REQ-004 / DES-007 | 地面あり。地上プレイヤー (y=208)、vy=0 | `jump_pressed` で 1 回 | vy == -330、y == 202.5、`on_ground` が偽 | 正常 | -345+15=-330、-330*(1/60)=-5.5 |
| TC-047 | G12 ジャンプ | REQ-005 / DES-007 | 地面なし。空中のプレイヤー (y=100)、`on_ground` が偽、vy が -100 と 100 | `jump_pressed` で 1 回 | vy が -85 と 115 | 異常 | 重力だけが働く |
| TC-048 | G12 ジャンプ | REQ-006 / DES-007 | 地面あり。地上プレイヤー (y=208) | (a) 1 回目だけ `jump_pressed`、(b) 毎回 `jump_pressed`、で 40 回 | どちらも y の最小値が 144.75（上昇量 63.25 px） | 境界 | 23 回で最高点。(23*345-15*276)/60=63.25 |
| TC-049 | G12 ジャンプ | REQ-011 / DES-007 | row 14 の col 0〜5 だけ床。地上プレイヤー (x=84) | 右入力で 12 回、続けて 1 回 | 12 回目に `on_ground` が偽・vy == 15・y == 208.25、13 回目に vy == 30 | 状態遷移 | 12 回後 x=84+5.6+7.5=97.1 で床から外れる。11 回後は x=95.6 で接地のまま |
| TC-050 | G13 敵の基本 | REQ-012 / DES-008 | なし | `create_enemy(WALKER, 100, 208)` と `create_enemy(KOOPA, 100, 208)` | state が WALKING、direction が -1、alive が真、box が (100, 208, 16, 16) | 正常 | |
| TC-051 | G13 敵の基本 | REQ-012, REQ-018 / DES-008 | 地面あり。地上の敵 (x=100)。種類 WALKER と KOOPA、direction が -1 と +1 | `update_enemy` を 1 回 | vx が -30 と 30、x が 99.5 と 100.5 | 正常 | 30*(1/60)=0.5 |
| TC-052 | G13 敵の基本 | REQ-012 / DES-008 | 地面あり。WALKER を (100, 207.9) に置く | `update_enemy` を 1 回 | y == 208、`on_ground` が真 | 正常 | 207.9+0.25 の下端 224.15 が床 224 を超える |
| TC-053 | G13 敵の基本 | REQ-019 / DES-008 | 地面あり。SHELL_IDLE の KOOPA (x=100) | `update_enemy` を 10 回 | x == 100、vx == 0 | 正常 | |
| TC-054 | G13 敵の基本 | REQ-049 / DES-008 | 地面あり。SHELL_SLIDING の KOOPA、WALKING の KOOPA、SHELL_IDLE の KOOPA | それぞれ `update_enemy` を 3 回 | `slide_age` が 3, 0, 0 | 状態遷移 | 滑走中だけ増える |
| TC-055 | G14 敵の反転 | REQ-013 / DES-008 | 地面あり。WALKING の敵。(a) col 5 の row 12・13 が壁（x 80〜96）、WALKER の direction=-1・x=96.2。(b) col 10 の row 12・13 が壁（x 160〜176）、direction=+1・x=143.8 | `update_enemy` を 1 回 | (a) x == 96、direction == +1、vx == 30。(b) x == 144、direction == -1、vx == -30 | 正常 | (a) 96.2-0.5=95.7 は壁に入り 96 に戻る。(b) 143.8+0.5=144.3 で右端 160.3 |
| TC-056 | G14 敵の反転 | REQ-014 / DES-008 | row 14 の col 0〜9 だけ床（x<160）。地上の敵、direction=+1。(種類, x) = (WALKER, 142.9), (WALKER, 143.0), (KOOPA WALKING, 143.0) | `update_enemy` を 1 回 | (direction, x) が (+1, 143.4), (-1, 142.5), (-1, 142.5)。いずれも `on_ground` が真 | 境界 | 足元の判定位置は右端+1。142.9+17=159.9 は床、143.0+17=160 は床なし |
| TC-057 | G14 敵の反転 | REQ-014 / DES-008 | row 14 の col 10〜19 だけ床（x≥160）。地上の WALKER、direction=-1。x が 161.0 と 160.9 | `update_enemy` を 1 回 | (direction, x) が (-1, 160.5) と (+1, 161.4) | 境界 | 判定位置は左端-1。161-1=160 は床、160.9-1=159.9 は床なし |
| TC-058 | G14 敵の反転 | REQ-021 / DES-008 | 地面あり。SHELL_SLIDING の KOOPA。(a) col 5 の row 12・13 が壁、direction=-1・x=96.5。(b) col 10 の row 12・13 が壁、direction=+1・x=143.5 | `update_enemy` を 1 回 | (a) x == 96、direction == +1、vx == 200。(b) x == 144、direction == -1、vx == -200 | 正常 | (a) 96.5-3.33=93.17 で壁に入る。(b) 143.5+3.33=146.83 で右端 162.83 |
| TC-059 | G14 敵の反転 | REQ-021 / DES-008 | row 14 の col 0〜9 だけ床。SHELL_SLIDING の KOOPA (x=157)、direction=+1、`on_ground` が真 | `update_enemy` を 1 回 | direction == +1、vx == 200、`on_ground` が偽、vy == 15 | 状態遷移 | 滑走する甲羅は崖で反転せず落ちる。157+3.33=160.33 は床の外 |
| TC-060 | G15 敵の状態遷移 | REQ-015 / DES-008 | WALKING の WALKER | `stomp_enemy(enemy)` | alive が偽 | 正常 | |
| TC-061 | G15 敵の状態遷移 | REQ-019, REQ-023 / DES-008 | WALKING の KOOPA。SHELL_SLIDING で `slide_age`=30 の KOOPA | `stomp_enemy(enemy)` | どちらも state が SHELL_IDLE、vx が 0、`slide_age` が 0、alive が真 | 状態遷移 | |
| TC-062 | G15 敵の状態遷移 | REQ-020 / DES-008 | SHELL_IDLE の KOOPA（中心 x=108）。プレイヤー中心 x が 96, 120, 108 | `kick_shell(enemy, player_center_x)` | (direction, vx) が (+1, 200), (-1, -200), (+1, 200)。state が SHELL_SLIDING、`slide_age` が 0 | 境界 | 向きは (甲羅の中心 - プレイヤー中心) の符号。0 のときは右 |
| TC-063 | G16 踏みつけ | REQ-015 / DES-009 | WALKER (100, 208)。プレイヤー (102, 196)、vy=100 | `resolve_player_enemies` | WALKER の alive が偽、`player_died` が偽 | 正常 | プレイヤー下端 212 が敵の上面 208 より下で、上半分（216 以下）にある |
| TC-064 | G16 踏みつけ | REQ-015 / DES-009 | WALKER (100, 208)。プレイヤー y が 199.9, 200.0, 200.1、vy=100 | `resolve_player_enemies` | 踏みつけ成立, 成立, 不成立。不成立では `player_died` が真で WALKER の alive が真 | 境界 | 下端 215.9 / 216.0 / 216.1。216=208+16*0.5 |
| TC-065 | G16 踏みつけ | REQ-015 / DES-009 | WALKER (100, 208)。プレイヤー (102, 196)、vy が 0 と -50 | `resolve_player_enemies` | `player_died` が真、WALKER の alive が真 | 異常 | 下降中でなければ踏みつけにならない |
| TC-066 | G16b 踏みつけの結果 | REQ-016 / DES-009 | WALKER (100, 208)。プレイヤー (102, 196)、vy=100 | `resolve_player_enemies` | プレイヤーの vy == -200、y == 192 | 正常 | 下端を敵の上面 208 に合わせる。重なりが残らない |
| TC-067 | G16b 踏みつけの結果 | REQ-019 / DES-009 | WALKING の KOOPA (100, 208)。プレイヤー (102, 196)、vy=100 | `resolve_player_enemies` | KOOPA の state が SHELL_IDLE、vx が 0、alive が真。`player_died` が偽、プレイヤーの vy が -200 | 状態遷移 | |
| TC-068 | G17 接触死亡 | REQ-017 / DES-009 | WALKER (100, 208)。プレイヤー x が 90 と 110、y=208、vy=0。KOOPA WALKING でも同じ | `resolve_player_enemies` | `player_died` が真、敵の alive が真 | 正常 | 90〜102 と 110〜122 が 100〜116 と重なる |
| TC-069 | G17 接触死亡 | REQ-017 / DES-009 | WALKER (100, 208)。プレイヤー (102, 218)、vy=-50 | `resolve_player_enemies` | `player_died` が真 | 正常 | 下から。218〜234 が 208〜224 と重なる |
| TC-070 | G17 接触死亡 | REQ-017 / DES-009 | WALKER (100, 208)。プレイヤー x が 60 と 88、y=208、vy=0 | `resolve_player_enemies` | `player_died` が偽、敵の alive が真、プレイヤーの vy が 0 のまま | 境界 | x=88 は右端 100 で接するだけ |
| TC-071 | G17 接触死亡 | REQ-017 / DES-009 | alive が偽の WALKER (100, 208)。プレイヤー (90, 208)、vy=0 | `resolve_player_enemies` | `player_died` が偽 | 異常 | 消えた敵は無視する |
| TC-072 | G17 接触死亡 | REQ-015, REQ-017 / DES-009 | WALKER A (100, 208) と WALKER B (112, 196)。プレイヤー (108, 196)、vy=100。リストの順は [A, B] と [B, A] | `resolve_player_enemies` | どちらの順でも A の alive が偽、B の alive が真、`player_died` が真 | 状態遷移 | B は下端 212 > 204 で踏みつけでない。A を踏んだ後 (y=192) も B と重なる。順序に依存しない |
| TC-073 | G18 甲羅 | REQ-020 / DES-009 | SHELL_IDLE の KOOPA (100, 208)。(プレイヤー位置, vy) = ((90,208), 0), ((110,208), 0), ((102,196), 100) | `resolve_player_enemies` | (state, direction, vx) が (SHELL_SLIDING, +1, 200), (SHELL_SLIDING, -1, -200), (SHELL_SLIDING, +1, 200)。`player_died` が偽。3 つ目はプレイヤーの vy が 100 のまま・y が 196 のまま | 状態遷移 | 上から触れても跳ね返らない。中心 x 108 とプレイヤー中心 108 は同じで右向き |
| TC-074 | G18 甲羅 | REQ-023 / DES-009 | SHELL_SLIDING の KOOPA (100, 208)、`slide_age`=30。プレイヤー (102, 196)、vy=100 | `resolve_player_enemies` | KOOPA の state が SHELL_IDLE、vx が 0。`player_died` が偽、プレイヤーの vy が -200 | 状態遷移 | |
| TC-075 | G18 甲羅 | REQ-024, REQ-049 / DES-009 | SHELL_SLIDING の KOOPA (100, 208)。プレイヤー (90, 208)、vy=0。`slide_age` が 0, 11, 12, 13, 14, 100 | `resolve_player_enemies` | `player_died` が 偽, 偽, 偽, 真, 真, 真 | 境界 | `slide_age` ≤ 12 は無害、> 12 は死亡 |
| TC-076 | G18 甲羅 | REQ-022 / DES-009 | SHELL_SLIDING の KOOPA (100, 208) と WALKER (110, 208)。リストの順は 2 通り | `resolve_shells_vs_walkers` | WALKER の alive が偽、KOOPA の state が SHELL_SLIDING のまま | 正常 | 順序に依存しない |
| TC-077 | G18 甲羅 | REQ-022 / DES-009 | (a) SHELL_SLIDING の KOOPA (100, 208) と WALKING の KOOPA (110, 208)。(b) SHELL_SLIDING の KOOPA と SHELL_IDLE の KOOPA (110, 208)。(c) SHELL_IDLE の KOOPA (100, 208) と WALKER (110, 208) | `resolve_shells_vs_walkers` | 3 件とも 2 体の alive が真で、state も変わらない | 異常 | 倒せるのは「滑走する甲羅が歩行敵に触れたとき」だけ |
| TC-078 | G19 カメラ | REQ-039 / DES-010 | prev=0、レベル幅 3200。プレイヤー中心 x が 100, 127, 128, 129, 200 | `next_camera_x` | 0, 0, 0, 1, 72 | 境界 | center-128 が正になる分だけ増える |
| TC-079 | G19 カメラ | REQ-040 / DES-010 | prev=500、プレイヤー中心 x=300 | `next_camera_x` | 500 | 異常 | 左へ戻らない |
| TC-080 | G19 カメラ | REQ-041 / DES-010 | レベル幅 3200。(prev, center) = (0, 3190), (2608, 100), (0, 0) | `next_camera_x` | 2608, 2608, 0 | 境界 | 3200-592=2608 |
| TC-081 | G20 Level 基本 | REQ-048 / DES-011 | 地面あり、`P` (2,13)、`W` (10,13) のステージ | `Level(data)` を作る | player の box が (34, 208, 12, 16)、enemies が 1 体で box が (160, 208, 16, 16)、`camera_x` が 0、status が PLAYING | 正常 | 配置規則（§0） |
| TC-082 | G20 Level 基本 | REQ-051 / DES-011 | TC-081 のレベル。`camera_x=100`・プレイヤーの x=87.9 にして `step` し、PLAYER_DIED にしたもの | もう 1 回 `step`（右入力） | status が PLAYER_DIED のまま、`coins_gained` が 0、プレイヤーの x と y が変わらない | 状態遷移 | PLAYING 以外では進めない |
| TC-083 | G20 Level 基本 | - / DES-011 | 地面なし、`P` (2,13)、`W` (10,14) のステージ | 入力なしで `step` を 10 回、続けて 1 回 | 10 回目までは enemies が 1 体、11 回目に 0 体。11 回目の status は PLAYING で、プレイヤーの y が 224.5 | 境界 | 敵の y = 224 + 0.125*n*(n+1)。n=10 で 237.75（240 以下）、n=11 で 240.5（上端 > 240）。プレイヤーは 208 + 0.125*11*12 = 224.5 |
| TC-084 | G21 Level ブロック | REQ-025, REQ-026 / DES-011 | 地面あり、`P` (2,13)、`?` (2,12) のステージの接地済みの Level。プレイヤーの頭がブロックの下面に接している | `jump_pressed` で `step` を 1 回 | `coins_gained` が 1、`tilemap.tile_at(2,12)` が USED | 正常 | ブロックの下面 208 = プレイヤーの上面 208。上昇すると頭が当たる |
| TC-085 | G21 Level ブロック | REQ-027 / DES-011 | TC-084 の後。入力なしで 1 回 `step`（再び接地）してから | `jump_pressed` で `step` を 1 回 | `coins_gained` が 0、`tile_at(2,12)` が USED のまま | 異常 | |
| TC-086 | G21 Level ブロック | REQ-025 / DES-011 | 地面あり、`P` (2,13)、`#` (2,12) のステージ | `jump_pressed` で `step` を 1 回 | `coins_gained` が 0、`tile_at(2,12)` が SOLID のまま | 異常 | ?ブロックだけがコインを出す |
| TC-087 | G22 Level 判定 | REQ-030 / DES-011 | 地面なし、`P` (2,13) のステージ | 入力なしで `step` を 15 回、続けて 1 回 | 15 回目まで PLAYING で y が 238、16 回目に PLAYER_DIED で y が 242 | 境界 | y = 208 + 0.125*n*(n+1)。n=15 で 238（240 以下）、n=16 で 242（240 超） |
| TC-088 | G22 Level 判定 | REQ-034 / DES-011 | 地面あり、`P` (7,13)、`F` (8,10)〜(8,13) のステージ（旗は x 128〜144） | 右入力で `step` を 5 回 | 4 回目まで PLAYING、5 回目に CLEARED | 境界 | 4 回目 x=116 で右端 128 が接するだけ。5 回目 x=117 で重なる（114+0.1*n*(n+1)） |
| TC-089 | G22 Level 判定 | REQ-017 / DES-011 | 地面あり、`P` (2,13)、`W` (3,13) のステージ | 右入力で `step` を 3 回 | 2 回目まで PLAYING、3 回目に PLAYER_DIED | 境界 | 3 回目: プレイヤー右端 47.2、敵 x=46.5 で重なる。2 回目: 46.6 と 47.0 で重ならない |
| TC-090 | G22 Level 判定 | REQ-015, REQ-016 / DES-011 | 地面あり、`P` (3,10)、`W` (3,13) のステージ | 入力なしで `enemies` が空になるまで `step` を繰り返す | 16 回目で空になり、status が PLAYING、プレイヤーの vy が -200、y が 192 | 回帰 | 16 回目に下端 210 が敵の上面 208 を超える（176+0.125*16*17=210）。vy は 240 に達している |
| TC-091 | G22 Level 判定 | REQ-051 / DES-011 | 地面あり、`P` (2,13)、`W` (10,13) のステージ。(camera_x, プレイヤー x) = (100, 87.9), (100, 88.0), (100, 88.1), (0, 0) | 入力なしで `step` を 1 回 | status が PLAYER_DIED, PLAYER_DIED, PLAYING, PLAYING | 境界 | プレイヤー右端 99.9 / 100.0 / 100.1 / 12。右端 ≤ カメラ x で死亡 |
| TC-092 | G23 Session 画面 | REQ-035 / DES-012 | なし | `GameSession(stage)` を作る | screen が TITLE | 正常 | |
| TC-093 | G23 Session 画面 | REQ-029, REQ-036 / DES-012 | TITLE の Session（地面あり、`P` (2,13) のステージ） | `jump_pressed` で `update` を 1 回 | screen が PLAYING、lives が 3、coins が 0、score が 0。プレイヤーが (34, 208) のまま | 状態遷移 | この更新では Level は進まない |
| TC-094 | G23 Session 画面 | REQ-036 / DES-012 | TITLE の Session | `jump_pressed` が偽で left, right, run が真の入力で `update` を 5 回 | screen が TITLE のまま | 異常 | Z だけが開始操作 |
| TC-095 | G23 Session 画面 | REQ-037 / DES-012 | screen が CLEAR の Session と GAME_OVER の Session | (a) `jump_pressed` で `update`、(b) `jump_pressed` なしで `update` | (a) screen が TITLE、(b) screen が元のまま | 状態遷移 | 2 画面 x 2 操作を parametrize |
| TC-096 | G23 Session 画面 | REQ-029 / DES-012 | screen が TITLE で lives=0、coins=7、score=900 の Session | `jump_pressed` で `update` | lives が 3、coins が 0、score が 0、screen が PLAYING | 回帰 | 再プレイで値が引き継がれない |
| TC-097 | G24 Session プレイ | REQ-028 / DES-012 | 地面あり、`P` (2,13)、`?` (2,12) のステージ。接地済みの Session（PLAYING）で coins=2、score=500 | `jump_pressed` で `update` を 1 回 | coins が 3、score が 600 | 正常 | +100 |
| TC-098 | G24 Session プレイ | REQ-031 / DES-012 | PLAYING の Session。lives が 3 と 2。Level の `camera_x` を 200 にする | 入力なしで `update` を 1 回 | lives が 2 と 1、screen が PLAYING | 状態遷移 | プレイヤー右端 46 ≤ 200 で死亡 |
| TC-099 | G24 Session プレイ | REQ-032 / DES-012 | PLAYING の Session。右入力で 5 回 `update` してプレイヤーが x=37 に動いた後、`camera_x` を 200 にする | 入力なしで `update` を 1 回 | プレイヤーが (34, 208)、`level.camera_x` が 0 | 状態遷移 | 新しい Level の開始位置 |
| TC-100 | G24 Session プレイ | REQ-048 / DES-012 | 地面あり、`P` (2,13)、`W` (10,13)、`?` (2,12) のステージ。接地済みの Session で `jump_pressed` を 1 回入れて ?ブロックを叩き（USED）、入力なしで 2 回進め、`camera_x` を 200 にする | 入力なしで `update` を 1 回 | `tile_at(2,12)` が QUESTION、敵が 1 体で box が (160, 208, 16, 16) | 回帰 | 敵は歩いて動いていたが初期位置に戻る |
| TC-101 | G24 Session プレイ | REQ-050 / DES-012 | TC-100 と同じ操作 | `update` を 1 回 | coins が 1、score が 100 | 回帰 | 死亡の前に得た値を保つ |
| TC-102 | G25 Session 終了 | REQ-033 / DES-012 | PLAYING の Session。lives が 1 | `camera_x` を 200 にして `update` を 1 回 | lives が 0、screen が GAME_OVER | 境界 | 残機 2 → 1 は PLAYING のまま（TC-098） |
| TC-103 | G25 Session 終了 | REQ-034 / DES-012 | 地面あり、`P` (7,13)、`F` (8,10)〜(8,13) のステージ。PLAYING の Session | 右入力で `update` を 5 回 | 4 回目まで screen が PLAYING、5 回目に CLEAR | 状態遷移 | TC-088 と同じ位置関係 |
| TC-104 | G25 Session 終了 | REQ-038 / DES-013 | lives=3、coins=0、score=0 の Session | `build_hud(session)` | lives が "LIFE 3"、coins が "COIN 0"、score が "SCORE 0" | 正常 | |
| TC-105 | G25 Session 終了 | REQ-038 / DES-013 | lives=2、coins=12、score=1200 の Session | `build_hud(session)` | "LIFE 2", "COIN 12", "SCORE 1200" | 正常 | 桁埋めなし |
| TC-106 | G26 描画の純粋部分 | REQ-044 / DES-015 | なし | `default_layout()` | 4 つのボタンそれぞれの左端 >= 0、右端 <= 592、上端 >= 0、下端 <= 304 | 正常 | 4 通りを parametrize。内部解像度 592x304 の中に収まる |
| TC-107 | G26 描画の純粋部分 | REQ-045 / DES-015 | `default_layout()`。left, right, jump, run それぞれの中心座標 | `points_to_held([中心])` | その 1 つのボタンだけが真 | 正常 | 4 通りを parametrize |
| TC-108 | G26 描画の純粋部分 | REQ-045 / DES-015 | `TouchLayout(left=(0,100,40,40), right=(50,100,40,40), jump=(200,100,40,40), run=(150,100,40,40))` | `points_to_held` を (a) [(0,100)]、(b) [(40,100)]、(c) [(39.9,139.9)]、(d) [(20,120),(220,120)]、(e) [] で呼ぶ | (a) left のみ真、(b) すべて偽、(c) left のみ真、(d) left と jump が真、(e) すべて偽 | 境界 | 左・上の辺は含み、右・下の辺は含まない |
| TC-109 | G26 描画の純粋部分 | REQ-045 / DES-014 | 全キーが未押下の `defaultdict(bool)`。K_LEFT, K_RIGHT, K_z, K_x を 1 つずつ真にしたもの | `keys_to_held(pressed)` と、`default_layout()` の対応するボタン中心での `points_to_held` を比べる | 4 通りとも等しい（左, 右, ジャンプ, ダッシュ）。K_a だけを真にしたときはすべて偽 | 正常 | キーもタッチも同じ HeldButtons になる |
| TC-110 | G26 描画の純粋部分 | REQ-046 / DES-014 | ブラウザでない環境（このテストの実行環境） | `detect_touch_device()` | 偽 | 正常 | |
| TC-111 | G27 定数・倍率・データ | REQ-102 / DES-016 | なし | `compute_scale(w, h)` を (592,304), (1184,608), (888,456), (1184,304), (592,608), (812,375) で呼ぶ | 1.0, 2.0, 1.5, 1.0, 1.0, 375/304（約 1.2336） | 境界 | min(w/592, h/304)。(1184,304) は高さ側、(592,608) は幅側が小さい。(812,375) は iPhone 12 mini の横向き相当で、375/304 が 812/592 より小さい。`pytest.approx` で比べる |
| TC-112 | G27 定数・倍率・データ | REQ-101 / DES-001 | なし | `FIXED_DT` を読む | 1/60 | 正常 | |
| TC-113 | G27 定数・倍率・データ | REQ-102 / DES-001 | なし | `SCREEN_W` と `SCREEN_H` を読む | 592 と 304 | 正常 | |
| TC-115 | G12 ジャンプ | REQ-004 / DES-007 | 地面あり。地上プレイヤー (y=208)、vy=0 | `jump_pressed` なしで（run なし）`update_player` を 1 回 | vy == 0、y == 208、`on_ground` が真 | 異常 | 押していなければ跳ばない。重力 15 で 0.25 沈み、床で 208 に戻る |
| TC-116 | G19 カメラ | REQ-039, REQ-041 / DES-010 | レベル幅 3200。(prev, center) = (500, 700), (500, 2735), (500, 2736), (500, 3500) | `next_camera_x` | 572, 2607, 2608, 2608 | 境界 | 700-128=572、2735-128=2607、2736-128=2608（最大 3200-592）、3500 は最大値に収める |
| TC-117 | G11b 水平移動の補足 | REQ-001 / DES-007 | 地面なし。空中のプレイヤー (y=100)、vx=0 | 右入力で `update_player` を 1 回 | vx == 12 | 正常 | 空中も ACCEL 720 で加速する。720*(1/60)=12 |
| TC-118 | G11b 水平移動の補足 | REQ-002 / DES-007 | 地面あり。地上プレイヤー、右入力のみ（run なし）。vx が 150 と 92 | `update_player` を 1 回 | vx が 135 と 90 | 境界 | 最大より速い間は DECEL 900 で減速し、最大 90 を下回らない。150-15=135、92-15=77 は 90 に収める |
| TC-119 | G16b 踏みつけの結果 | REQ-015 / DES-009 | WALKER (100, 208)。プレイヤー (x, y) = (70, 196), (102, 192), (102, 192.1)、vy=100 | `resolve_player_enemies` | 接触なし, 接するだけ, 踏みつけ成立。前の 2 つは `player_died` が偽・WALKER の alive が真・プレイヤーの vy が 100 のまま。3 つ目は alive が偽・`player_died` が偽 | 境界 | x=70 は 70〜82 で 100〜116 と重ならない。y=192 は下端 208 で敵の上面に接するだけ。192.1 は 0.1 px 重なる |
| TC-120 | G22b Level 判定の補足 | REQ-034, REQ-051 / DES-011 | 地面あり、`P` (2,13)、`F` (5,12) と (5,13)（旗は x 80〜96）のステージの Level。`camera_x`=100、プレイヤーの x=88 | 入力なしで `step` を 1 回 | status が PLAYER_DIED | 境界 | 旗と x 88〜96 で重なるが、同時に右端 100 ≤ camera_x 100 で死亡。死亡が優先 |
| TC-121 | G22b Level 判定の補足 | REQ-034 / DES-011 | TC-088 の Level を右入力で 5 回進めて CLEARED にしたもの | 右入力で `step` を 1 回 | status が CLEARED のまま、`coins_gained` が 0、プレイヤーの x が変わらない | 状態遷移 | PLAYING 以外では進めない |
| TC-122 | G22b Level 判定の補足 | REQ-039 / DES-011 | 地面なし、`P` (20,13) のステージの Level。入力なしで 15 回進めた後、`camera_x` を 0 にする | 入力なしで `step` を 1 回（16 回目で死亡） | status が PLAYER_DIED、`camera_x` が 200 | 状態遷移 | プレイヤー中心 x=322+6=328、328-128=200。死亡したフレームでもカメラは更新される |
| TC-123 | G26b 仮想ボタンの配置 | REQ-053 / DES-015 | なし | `default_layout()` | 4 つのボタンそれぞれの上端 >= 240、下端 <= 304 | 境界 | 4 通りを parametrize。操作パネルは y=240〜304（境界の 240 を含む） |
| TC-124 | G26b 仮想ボタンの配置 | REQ-056 / DES-015 | なし | `default_layout()` の 4 つから 2 つを選ぶ 6 通り | どの 2 つの矩形も重ならない（片方の右端 <= もう片方の左端、または下端 <= 上端） | 正常 | 6 通りを parametrize。辺が接するだけは重ならない扱い |
| TC-125 | G26b 仮想ボタンの配置 | REQ-056 / DES-015 | なし | `default_layout()` | 4 つのボタンそれぞれの幅 >= 48 かつ高さ >= 48 | 境界 | 4 通りを parametrize。境界の 48 を含む |
| TC-126 | G27b 画面寸法・倍率の補足 | REQ-052, REQ-054 / DES-001 | なし | `PLAY_H` と `PANEL_H` を読む | 240 と 64 | 正常 | y=0〜240 がステージ領域、y=240〜304 が操作パネル |
| TC-127 | G27b 画面寸法・倍率の補足 | REQ-102 / DES-016 | なし | `compute_scale(w, h)` を (0, 304), (592, 0), (0, 0) で呼ぶ | 0.0, 0.0, 0.0 | 異常 | 幅か高さが 0 のウィンドウでは倍率 0.0（例外にしない） |
| TC-128 | G27b 画面寸法・倍率の補足 | REQ-056 / DES-001 | なし | `TOUCH_BUTTON_SIZE` を読む | 48 | 正常 | |
| TC-129 | G28 穴の列の判定 | REQ-052, REQ-057 / DES-016 | 最下段（row 14）をすべて `#` にし、(10,14) と (11,14) だけ `.` にしたステージの TileMap | `column_has_ground(tilemap, col)` を col = 9, 10, 11, 12 で呼ぶ | True, False, False, True | 境界 | 4 通りを parametrize。穴（10, 11）の前後の列は地面 |
| TC-130 | G28 穴の列の判定 | REQ-057 / DES-016 | 最下段は空で、(20,13) だけ `#` のステージの TileMap | `column_has_ground(tilemap, 20)` | False | 異常 | 最下段のマスだけを見る。row 13 が固体でも穴の列として扱う |
| TC-131 | G28 穴の列の判定 | REQ-052 / DES-016 | 最下段が空のステージの TileMap | `column_has_ground(tilemap, col)` を col = -1, 200 で呼ぶ | True, True | 境界 | 2 通りを parametrize。ステージの左右の外は壁（`is_solid` の仕様）なので地面の列として扱う |

## 2. 手動確認（自動化しないもの）
| ID | 確認内容 | 合格基準 | 対応 REQ |
|---|---|---|---|
| MC-001 | プレイ画面の見た目 | 残機・コイン数・スコアが画面上部に読める大きさで表示され、値がプレイ中の変化と一致する | REQ-038 |
| MC-002 | iPhone で起動する | 仮想ボタン（左・右・ジャンプ・ダッシュ）が横向きの画面の下の操作パネルに表示され、親指で押せる。画面は横長の長方形で、正方形に近い表示ではない | REQ-044, REQ-102 |
| MC-003 | macOS で起動する | 仮想ボタンが表示されない。下の操作パネルは地面の絵で表示される | REQ-046, REQ-055 |
| MC-004 | 素材の出所 | `assets/` の全画像が `docs/assets/ASSETS.md` に出所と CC0 のライセンスつきで載っている | REQ-047 |
| MC-005 | 更新処理の時間 | `Level.step` を 1000 回呼んだ 1 回あたりの平均が 16.6 ms 以下（実測値を記録） | REQ-101 |
| MC-006 | macOS の Chrome（最新版） | Web 版でタイトル画面から旗に触れてクリア画面まで遊べる。ウィンドウの大きさを変えても縦横比 592:304 が保たれ、ウィンドウに収まる最大の大きさで表示される | REQ-102, REQ-103 |
| MC-007 | iPhone 12 mini（最新 iOS）の Safari | Web 版が横向きのままタイトル画面からクリア画面まで遊べる | REQ-104 |
| MC-008 | 開発機でのローカル起動 | `.venv/bin/python -m src.main` でタイトル画面が表示される | REQ-105 |
| MC-009 | 操作感 | 歩行・ダッシュ・ジャンプ・減速が意図どおりと感じる | REQ-001, REQ-002, REQ-003, REQ-004 |
| MC-011 | ステージファイル | `.venv/bin/python -c` で `assets/stages/stage1.txt` を `parse_stage` に渡して例外なく解析でき、歩行敵・甲羅敵・?ブロックが 1 つ以上あり、row 14 に穴が 1 つ以上ある | REQ-042, REQ-043 |
| MC-012 | 描画フレームに複数ステップが走る場合 | 実時間を遅らせて 1 描画フレームに 2 ステップ以上走らせ、Z を 1 回押したときジャンプが 1 回だけ起きる。1 描画フレームで消化するステップ数が 5 を超えない | REQ-004, REQ-101 |
| MC-013 | macOS の Chrome で画面の構成を見る | 画面の下 64 px（全体の下 21%）が地面の絵の操作パネルになっている。ステージの地面の続きとして、地面の列の下は地面の絵で表示される。ステージのタイルと旗と残機・コイン数・スコアの表示が、操作パネルの中へ描かれない。残機・コイン数・スコアが操作パネルの外（上側）に表示される | REQ-052, REQ-054, REQ-055 |
| MC-014 | iPhone 12 mini の横向きで仮想ボタンを見る | 4 つのボタンが操作パネルの中に収まり、ステージの地面やプレイヤー・敵と重ならない。それぞれのボタンを指で押すと、押した位置のボタンだけが反応する（拡大が小数倍でも位置がずれない） | REQ-053, REQ-056, REQ-044, REQ-102 |
| MC-015 | macOS の Chrome で穴の見た目を見る | 穴の列では、ステージの地面の下から画面の下端（y=304）まで黒で、深い穴に見える（地面の列だけ地面の絵）。プレイヤーが穴に落ちる間、y=240 の線で消えず、操作パネルの高さの黒の中へ落ちていく様子が見える。穴に落ちる敵も同様に見える | REQ-057, REQ-058, REQ-052 |
| MC-010 | 1面の通しプレイ | 開始位置から旗まで、穴・敵 2 種・?ブロックを含めて遊びきれる | REQ-034 |

## 3. トレーサビリティ
`.venv/bin/python scripts/trace_check.py --stage spec` の結果: OK（2026-11-13、ギャップ 0 件。変更要求 REQ-052〜058 を含む）。

注記: 手動確認（MC）でしか確認できない REQ-047, 103, 104, 105 を数えられるよう、`trace_check.py` の spec 検査で MC の行も「担当あり」と数える変更を入れた（tests 検査は TC の行のみ）。

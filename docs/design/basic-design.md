# 基本設計書

最終更新: 2026-11-13 / 状態: 変更要求 2 件目（穴を画面の下端まで通す）を反映中・レビューと人間の承認待ち（1 件目は承認済み）/ 対応要件: docs/requirements/requirements.md（REQ-001〜058, 101〜105）

## 1. 要件割当表（空欄禁止）
| REQ | 担当 DES | 備考 |
|---|---|---|
| REQ-001 | DES-007 | 水平加速・最大歩行速度 |
| REQ-002 | DES-007 | ダッシュ時の最大速度 |
| REQ-003 | DES-007 | 入力なしの減速 |
| REQ-004 | DES-007 | 地上でのジャンプ開始 |
| REQ-005 | DES-007 | 空中ではジャンプしない |
| REQ-006 | DES-007, DES-006 | 固定初速。重力適用順は §5 |
| REQ-007 | DES-006 | 落下速度の上限 |
| REQ-008 | DES-006 | 床への着地 |
| REQ-009 | DES-006, DES-005 | 壁の判定。ステージ左右端も壁 |
| REQ-010 | DES-006 | 天井衝突 |
| REQ-011 | DES-006, DES-007 | 毎フレーム重力を加える |
| REQ-012 | DES-008 | |
| REQ-013 | DES-008 | |
| REQ-014 | DES-008 | |
| REQ-015 | DES-009, DES-008 | 踏みつけ判定は DES-009 |
| REQ-016 | DES-009 | |
| REQ-017 | DES-009 | |
| REQ-018 | DES-008 | |
| REQ-019 | DES-009, DES-008 | |
| REQ-020 | DES-009, DES-008 | |
| REQ-021 | DES-008 | |
| REQ-022 | DES-009 | |
| REQ-023 | DES-009, DES-008 | |
| REQ-024 | DES-009 | |
| REQ-025 | DES-011, DES-005 | 天井衝突セルから?ブロック判定 |
| REQ-026 | DES-005 | |
| REQ-027 | DES-005 | |
| REQ-028 | DES-012 | |
| REQ-029 | DES-012 | |
| REQ-030 | DES-011 | |
| REQ-031 | DES-012 | |
| REQ-032 | DES-012 | |
| REQ-033 | DES-012 | |
| REQ-051 | DES-011 | 判定にはその時点のカメラ x を使う |
| REQ-034 | DES-011, DES-012 | 接触判定は DES-011、画面遷移は DES-012 |
| REQ-035 | DES-012 | |
| REQ-036 | DES-012 | |
| REQ-037 | DES-012 | |
| REQ-038 | DES-013, DES-016 | 値の整形は DES-013、描画は DES-016 |
| REQ-039 | DES-010 | |
| REQ-040 | DES-010 | |
| REQ-041 | DES-010 | 上限は level_width - SCREEN_W（SCREEN_W=592） |
| REQ-042 | DES-004, DES-019, DES-018 | 解析は DES-004、データは DES-019、読込は DES-018 |
| REQ-043 | DES-004, DES-019 | 解析時に寸法を検証 |
| REQ-044 | DES-015, DES-016 | |
| REQ-052 | DES-016, DES-001 | 下部 64 px を、最下段が地面の列だけ地面の絵で描く（ステージの地面の続き）。寸法は constants |
| REQ-053 | DES-015, DES-016 | 配置は DES-015（§6.1）、描画は DES-016 |
| REQ-054 | DES-016, DES-001 | ステージ本体のタイル・旗・HUD を y<240 にクリップして描く |
| REQ-055 | DES-016 | 操作パネルは touch_visible に関係なく描く |
| REQ-056 | DES-015 | ボタン配置が互いに重ならず 48 px 以上（§6.1） |
| REQ-057 | DES-016 | 最下段が空の列は操作パネルを黒で塗る。判定は `column_has_ground` |
| REQ-058 | DES-016 | プレイヤーと敵は操作パネルの後にクリップなしで描く |
| REQ-045 | DES-002, DES-014, DES-015 | キーもタッチも同じ HeldButtons に変換 |
| REQ-046 | DES-014, DES-016 | 端末判定は DES-014 |
| REQ-047 | DES-017 | 素材一覧 docs/assets/ASSETS.md |
| REQ-048 | DES-012, DES-011 | 再開時に Level を作り直す |
| REQ-049 | DES-009, DES-008 | 滑走開始からの経過フレームを敵が持つ |
| REQ-050 | DES-012 | コイン数・スコアは Session が持つ |
| REQ-101 | DES-018, DES-001 | 固定ステップ 1/60 |
| REQ-102 | DES-016, DES-001, DES-018 | 倍率の計算は DES-016、解像度は DES-001、拡大表示とタッチ座標の変換は DES-018 |
| REQ-103 | DES-018 | Web 版を Chrome で確認（手動） |
| REQ-104 | DES-018, DES-015 | Web 版を iPhone 12 mini で確認（手動） |
| REQ-105 | DES-018 | |

## 2. データモデル
座標は左上原点、x は右、y は下が正。単位は px、速度は px/s。

| 名前 | 場所 | 属性（型・単位） | 持ち主 |
|---|---|---|---|
| Aabb | src/game/geometry.py | x, y, w, h: float(px) | 各エンティティ |
| HeldButtons | src/game/input_state.py | left, right, jump, run: bool | render が描画フレームごとに作る。前回の jump は main が持つ |
| InputState | src/game/input_state.py | left, right, run: bool, jump_pressed: bool（押した瞬間のみ true） | Session.update の引数 |
| TileKind | src/game/stage_data.py | EMPTY / SOLID / QUESTION / USED | TileMap |
| StageData | src/game/stage_data.py | tiles: 行×列の TileKind, start: (col,row), walkers: [(col,row)], koopas: [(col,row)], flag: Aabb（読み込み後は不変） | main が保持し Session に渡す |
| TileMap | src/game/tilemap.py | StageData から複製したタイル（?ブロックの使用済み状態を含む） | Level |
| Body | src/game/physics.py | box: Aabb, vx, vy: float(px/s), on_ground: bool | Player / Enemy |
| Player | src/game/player.py | body: Body, alive: bool | Level |
| EnemyKind | src/game/enemy.py | WALKER / KOOPA | Enemy |
| EnemyState | src/game/enemy.py | WALKING / SHELL_IDLE / SHELL_SLIDING | Enemy |
| Enemy | src/game/enemy.py | kind, state, body, direction: int(-1/+1), slide_age: int(フレーム), alive: bool | Level |
| Level | src/game/level.py | player, tilemap, enemies: list[Enemy], flag: Aabb, camera_x: float(px), status: LevelStatus | Session |
| Screen | src/game/session.py | TITLE / PLAYING / CLEAR / GAME_OVER | Session |
| GameSession | src/game/session.py | screen, lives: int, coins: int, score: int, level: Level \| None | main |
| HudText | src/game/hud.py | lives, coins, score: str | 描画のたびに作る（保持しない） |

## 3. モジュール責務
| ID | モジュール | 責務（1文） | 依存してよいもの | 対応REQ |
|---|---|---|---|---|
| DES-001 | src/game/constants.py | 物理・寸法・得点の定数に名前と単位を与える | なし | REQ-052, REQ-054, REQ-101, REQ-102 |
| DES-002 | src/game/input_state.py | 押下状態（HeldButtons）から、押した瞬間を含む InputState を作る | なし | REQ-045 |
| DES-003 | src/game/geometry.py | 矩形の重なり判定とタイル番号の計算を提供する | constants | -（DES-006, 009 が利用する下位部品） |
| DES-004 | src/game/stage_data.py | ステージの文字列を検証して StageData に変換する | constants, geometry | REQ-042, REQ-043 |
| DES-005 | src/game/tilemap.py | タイルの固体判定と?ブロックの状態変更を担う | constants, stage_data | REQ-009, REQ-025, REQ-026, REQ-027 |
| DES-006 | src/game/physics.py | 重力の適用と、軸を分けたタイル衝突の解決を行う | constants, geometry, tilemap | REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011 |
| DES-007 | src/game/player.py | 入力と時間からプレイヤーの速度と位置を更新する | constants, input_state, physics | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-011 |
| DES-008 | src/game/enemy.py | 敵の移動・反転・状態遷移を更新する | constants, physics | REQ-012, REQ-013, REQ-014, REQ-015, REQ-018, REQ-019, REQ-020, REQ-021, REQ-023, REQ-049 |
| DES-009 | src/game/interactions.py | プレイヤーと敵、甲羅と歩行敵の接触結果を決める | constants, geometry, player, enemy | REQ-015, REQ-016, REQ-017, REQ-019, REQ-020, REQ-022, REQ-023, REQ-024, REQ-049 |
| DES-010 | src/game/camera.py | 次のカメラ x を計算する | constants | REQ-039, REQ-040, REQ-041 |
| DES-011 | src/game/level.py | 1フレームの更新を §5 の順に進め、結果（コイン・死亡・クリア）を返す | 上記すべて | REQ-025, REQ-030, REQ-034, REQ-048, REQ-051 |
| DES-012 | src/game/session.py | 画面遷移と残機・コイン・スコアを管理し、Level を作り直す | level, stage_data | REQ-028, REQ-029, REQ-031, REQ-032, REQ-033, REQ-034, REQ-035, REQ-036, REQ-037, REQ-048, REQ-050 |
| DES-013 | src/game/hud.py | 残機・コイン・スコアの表示文字列を作る | session | REQ-038 |
| DES-014 | src/render/input_mapper.py | キーボード状態を HeldButtons に変換し、タッチ端末かを判定する | game.input_state, pygame | REQ-045, REQ-046 |
| DES-015 | src/render/touch_controls.py | タッチ座標を仮想ボタンの HeldButtons に変換する | game.input_state | REQ-044, REQ-045, REQ-053, REQ-056, REQ-104 |
| DES-016 | src/render/renderer.py | Session の状態を、ステージ領域（上 240 px）・操作パネル（下 64 px）・プレイヤーと敵の順に内部解像度の面へ描き、表示倍率を計算する | game, assets, touch_controls, pygame | REQ-038, REQ-044, REQ-046, REQ-052, REQ-053, REQ-054, REQ-055, REQ-057, REQ-058, REQ-102 |
| DES-017 | src/render/assets.py | CC0 のドット絵を読み込み、出所を docs/assets/ASSETS.md に記録する | pygame | REQ-047 |
| DES-018 | src/main.py | 初期化・固定ステップのループ・ステージファイル読込・内部描画面の拡大表示・タッチ座標の変換を行う | render, game | REQ-042, REQ-101, REQ-102, REQ-103, REQ-104, REQ-105 |
| DES-019 | assets/stages/stage1.txt | 1面のタイル・敵・?ブロック・旗・開始位置を文字で記述する | - | REQ-042, REQ-043 |

### ステージファイルの文字
幅 200 文字 × 高さ 15 行。

| 文字 | 意味 |
|---|---|
| `.` | 空 |
| `#` | 固体（地面・壁・足場） |
| `?` | 中身のある?ブロック（固体） |
| `P` | プレイヤー開始位置（1つ） |
| `W` | 歩行敵の初期位置 |
| `K` | 甲羅敵の初期位置 |
| `F` | 旗（1つ以上。全 `F` セルを囲む矩形が旗の当たり判定） |

## 4. インターフェース
シグネチャと意味だけを書く。時間は `dt`（固定ステップ 1/60 秒）、入力は `InputState`、乱数は使わない。

```python
# geometry.py
@dataclass
class Aabb:
    x: float; y: float; w: float; h: float
    # 読み取り専用: left, right, top, bottom, center_x
    def overlaps(self, other: "Aabb") -> bool: ...   # 辺が接するだけは False

def tile_span(lo: float, hi: float) -> range:
    """区間 [lo, hi) が重なるタイル番号の範囲。floor で計算し、負の値でも正しい"""

# input_state.py
@dataclass(frozen=True)
class HeldButtons: left: bool; right: bool; jump: bool; run: bool
@dataclass(frozen=True)
class InputState: left: bool; right: bool; run: bool; jump_pressed: bool
def make_input(held: HeldButtons, prev_jump_held: bool) -> InputState:
    """jump_pressed = held.jump and not prev_jump_held"""
def merge_held(a: HeldButtons, b: HeldButtons) -> HeldButtons:   # 項目ごとの OR

# stage_data.py
class StageFormatError(ValueError): ...
def parse_stage(text: str) -> StageData:
    """200x15 でない・未知の文字・P が1つでない・F がない場合は StageFormatError"""

# tilemap.py
class TileMap:
    def __init__(self, data: StageData) -> None: ...
    def is_solid(self, col: int, row: int) -> bool:
        """col < 0 または col >= 幅 は True（ステージ左右端は壁）。row < 0 と row >= 高さ は False"""
    def tile_at(self, col: int, row: int) -> TileKind: ...
    def hit_question(self, col: int, row: int) -> bool:
        """QUESTION なら USED にして True。それ以外は変更せず False"""

# physics.py
@dataclass
class Body: box: Aabb; vx: float; vy: float; on_ground: bool
@dataclass(frozen=True)
class CollisionResult:
    hit_left: bool; hit_right: bool; hit_ceiling: bool
    ceiling_cell: tuple[int, int] | None   # 天井に当たったタイルのうち、box 中心 x に最も近いもの
def apply_gravity(body: Body, dt: float) -> None:
    """vy += GRAVITY*dt の後、FALL_MAX_SPEED で頭打ち"""
def move_and_collide(body: Body, tilemap: TileMap, dt: float) -> CollisionResult:
    """x 移動→x 解決→y 移動→y 解決の順。接触した軸の速度を 0 にし、on_ground を毎回再計算する"""

# player.py
@dataclass
class Player: body: Body; alive: bool
def create_player(x: float, y: float) -> Player: ...
def update_player(player: Player, inp: InputState, tilemap: TileMap, dt: float) -> CollisionResult: ...

# enemy.py
def create_enemy(kind: EnemyKind, x: float, y: float) -> Enemy: ...
def update_enemy(enemy: Enemy, tilemap: TileMap, dt: float) -> None:
    """重力・移動・崖と壁での反転・滑走経過フレームの加算を含め、敵を1ステップ進める"""
def stomp_enemy(enemy: Enemy) -> None:
    """WALKER は alive=False。KOOPA の WALKING / SHELL_SLIDING は SHELL_IDLE にして vx=0, slide_age=0"""
def kick_shell(enemy: Enemy, player_center_x: float) -> None:
    """SHELL_IDLE を SHELL_SLIDING にする。向きは (甲羅の中心 x − プレイヤー中心 x) の符号。0 のときは右"""

# interactions.py
@dataclass(frozen=True)
class PlayerEnemyResult: player_died: bool
def resolve_player_enemies(player: Player, enemies: list[Enemy]) -> PlayerEnemyResult:
    """alive=False の敵は無視する。踏みつけを先に全部処理し、その後に死亡接触を判定する。
    踏んだ敵に対しては、プレイヤーの下端を敵の上面に合わせ（重なりを解消）、vy = -STOMP_BOUNCE_SPEED にする"""
def resolve_shells_vs_walkers(enemies: list[Enemy]) -> None:
    """SHELL_SLIDING の甲羅に触れた WALKER を alive=False にする。alive=False の敵は無視する"""

# camera.py
def next_camera_x(prev: float, player_center_x: float, level_width: float) -> float:
    """プレイヤーに追従し、prev より小さくならず、0 以上かつ level_width - SCREEN_W 以下に収める"""

# level.py
class LevelStatus(Enum): PLAYING; PLAYER_DIED; CLEARED
@dataclass(frozen=True)
class LevelEvents: coins_gained: int; status: LevelStatus
class Level:
    def __init__(self, data: StageData) -> None: ...
    def step(self, inp: InputState, dt: float) -> LevelEvents:
        """status が PLAYING のときだけ進める。§5 の順序"""

# session.py
class GameSession:
    def __init__(self, stage: StageData) -> None: ...   # screen=TITLE
    def update(self, inp: InputState, dt: float) -> None:
        """TITLE / CLEAR / GAME_OVER では inp.jump_pressed だけを見る。TITLE から PLAYING へ移るとき lives/coins/score を初期値に戻す。PLAYING では Level.step の結果を反映する"""

# hud.py
def build_hud(session: GameSession) -> HudText:
    """lives="LIFE n", coins="COIN n", score="SCORE n"（n は 10 進数、桁埋めなし）"""

# render/input_mapper.py
def keys_to_held(pressed: Mapping[int, bool]) -> HeldButtons:   # ←→ / Z / X
def detect_touch_device() -> bool:
    """ブラウザ実行時は navigator.maxTouchPoints > 0。それ以外は False"""

# render/touch_controls.py
@dataclass(frozen=True)
class TouchLayout: left: Aabb; right: Aabb; jump: Aabb; run: Aabb   # 内部解像度の座標
def default_layout() -> TouchLayout:
    """§6.1 の配置を返す。4 つとも操作パネル内（y >= PLAY_H）で、互いに重ならず、幅と高さが TOUCH_BUTTON_SIZE"""
def points_to_held(points: Sequence[tuple[float, float]], layout: TouchLayout) -> HeldButtons:
    """点が入っているボタンを押下とみなす。複数点で複数ボタン"""

# render/renderer.py
def compute_scale(window_w: int, window_h: int) -> float:
    """min(window_w / SCREEN_W, window_h / SCREEN_H)。小数。ウィンドウの幅か高さが 0 のとき 0.0"""
def column_has_ground(tilemap: TileMap, col: int) -> bool:
    """最下段（row = STAGE_H_TILES - 1）のマスが固体なら True。穴の列は False。範囲外の列は TileMap.is_solid に従う"""
def draw(surface: pygame.Surface, session: GameSession, assets: Assets, touch_visible: bool) -> None:
    """描く順序:
    1. ステージ本体のタイル・旗・HUD・タイトル・クリア・ゲームオーバーの文字を、y < PLAY_H にクリップして描く
    2. 操作パネル（y = PLAY_H から SCREEN_H）を、タイルの列ごとに塗る。column_has_ground が真の列は地面のタイル、偽の列は黒。
       `session.screen` が PLAYING でない画面（タイトル・クリア・ゲームオーバー）では、Level の有無に関係なく全列を地面のタイルで塗る。touch_visible に関係なく常に塗る
    3. プレイヤーと敵を、クリップなしで描く（穴に落ちる間も操作パネルの高さまで見える）
    4. touch_visible のときだけ、仮想ボタンを描く"""

# main.py
async def main() -> None:
    """ステージファイルを読み、固定ステップでループする。1 フレームに実時間を最大 5 ステップ分まで消化する"""
```

## 5. 1フレームの更新順序
`main` は実時間の経過をためて、`FIXED_DT = 1/60` ずつ次を繰り返す。

| # | 担当 | 処理 |
|---|---|---|
| 1 | main（DES-018）と render（DES-014/015） | 描画フレームの冒頭で、キーボードとタッチの押下状態を HeldButtons に集める。`prev_jump_held` は main が持ち、描画フレームごとに1回だけ `make_input` で InputState にする。同じ描画フレームで複数ステップ走るときは、`jump_pressed` を最初のステップだけ true、以降のステップは false にする（他の項目は全ステップで同じ） |
| 2 | Session | 画面が TITLE / CLEAR / GAME_OVER なら Z（`jump_pressed`）だけを見て画面遷移して終わる |
| 3 | Level | プレイヤー更新: 水平加速・減速 → ジャンプ開始（接地かつ `jump_pressed`）→ `apply_gravity` → `move_and_collide` |
| 4 | Level | 天井に当たったセルが QUESTION なら `hit_question` を呼び、成功したらコイン +1 |
| 5 | Level | 敵更新: 全敵に `update_enemy`。ステージ下端より下に落ちた敵は取り除く |
| 6 | Level | `resolve_shells_vs_walkers` |
| 7 | Level | `resolve_player_enemies`（踏みつけ → 死亡接触の順。踏んだときはプレイヤーを敵の上面へ押し上げて重なりを解消する） |
| 8 | Level | 取り除かれた敵（`alive=False`）をリストから外す |
| 9 | Level | 判定: プレイヤー上端 > ステージ下端、プレイヤー右端 <= カメラ x（更新前の値）、または死亡接触なら PLAYER_DIED。旗に重なれば CLEARED。両方成立したら PLAYER_DIED |
| 10 | Level | `next_camera_x` でカメラ更新（死亡・クリアのフレームも更新する） |
| 11 | Session | TITLE から PLAYING へ移るときは、`lives=INITIAL_LIVES`、`coins=0`、`score=0` に戻して新しい Level を作る。PLAYING 中は、コインがあれば `coins` と `score`（+100/枚）を更新。PLAYER_DIED なら `lives` を 1 減らし、0 超なら新しい Level を作る（敵・?ブロック・開始位置が初期化され、coins/score は保つ）、0 なら GAME_OVER。CLEARED なら CLEAR |
| 12 | render | `build_hud` の文字列と Session / Level の状態を、ステージ領域（y < PLAY_H）にクリップして描く → 操作パネルを列ごとに描く（穴の列は黒）→ プレイヤーと敵を描く → 仮想ボタンを描く（タッチ端末のみ）。内部描画面は、縦横比を保ち小数倍で拡大して表示する |

## 6. 定数表（`src/game/constants.py` に集約）
| 名前 | 値 | 単位 | 出典 |
|---|---|---|---|
| SCREEN_W | 592 | px | REQ-102 |
| SCREEN_H | 304 | px | REQ-102 |
| PLAY_H | 240 | px | REQ-054（ステージの高さ。STAGE_H_TILES * TILE_SIZE と一致） |
| PANEL_H | 64 | px | REQ-052（SCREEN_H - PLAY_H と一致） |
| TOUCH_BUTTON_SIZE | 48 | px | REQ-056 |
| TILE_SIZE | 16 | px | 要件 §3 冒頭 |
| FIXED_DT | 1/60 | s | REQ-101 |
| MAX_STEPS_PER_FRAME | 5 | 回 | 初期値案（遅延時の暴走防止） |
| STAGE_W_TILES | 200 | タイル | REQ-043 |
| STAGE_H_TILES | 15 | タイル | REQ-043 |
| PLAYER_W | 12 | px | 初期値案 |
| PLAYER_H | 16 | px | 初期値案 |
| ENEMY_W | 16 | px | 初期値案 |
| ENEMY_H | 16 | px | 初期値案 |
| WALK_MAX_SPEED | 90 | px/s | REQ-001 |
| RUN_MAX_SPEED | 150 | px/s | REQ-002 |
| ACCEL | 720 | px/s^2 | 初期値案（0 から 90 まで 0.125 秒） |
| GROUND_DECEL | 900 | px/s^2 | 初期値案（REQ-003 を満たす） |
| AIR_DECEL | 360 | px/s^2 | 初期値案 |
| GRAVITY | 900 | px/s^2 | 初期値案 |
| JUMP_SPEED | 345 | px/s | REQ-006（速度を先に更新する順で最高到達点 63.25 px。計算で確認済み） |
| FALL_MAX_SPEED | 240 | px/s | REQ-007 |
| STOMP_BOUNCE_SPEED | 200 | px/s | 初期値案 |
| ENEMY_WALK_SPEED | 30 | px/s | REQ-012, REQ-018 |
| SHELL_SLIDE_SPEED | 200 | px/s | REQ-020 |
| SHELL_GRACE_FRAMES | 12 | フレーム | REQ-049 |
| COIN_SCORE | 100 | 点 | REQ-028 |
| INITIAL_LIVES | 3 | 機 | REQ-029 |
| CAMERA_FOLLOW_X | 128 | px | REQ-039 |
| STOMP_ZONE_RATIO | 0.5 | 比 | 要件 §5「踏みつけ条件」（敵の上半分） |

### 6.1 仮想ボタンの配置（`src/render/touch_controls.py`）
内部解像度の座標（左上原点）。縦位置は操作パネルの上端 240 px に余白 8 px を足した 248 px。

| ボタン | x | y | 幅 | 高さ | 出典 |
|---|---|---|---|---|---|
| left | 16 | 248 | 48 | 48 | REQ-053, REQ-056（初期値案） |
| right | 72 | 248 | 48 | 48 | 同上 |
| run | 472 | 248 | 48 | 48 | 同上 |
| jump | 528 | 248 | 48 | 48 | 同上 |

## 7. 設計判断
| # | 選択 | 代替案 | 理由 |
|---|---|---|---|
| 1 | Level（1回のプレイ中の状態）と GameSession（画面・残機・コイン・スコア）を分ける | 1つのクラスに全部持たせる | 再開時は Level だけ作り直せば REQ-048 が成り立ち、REQ-050 のコイン・スコア保持も自然に満たせる |
| 2 | ステージは文字列を解析する純関数 `parse_stage` とし、ファイル読込は `main.py` が行う | game 層でファイルを読む | game 層はファイルアクセス禁止（architecture.md）。テストで小さなステージ文字列を直接渡せる |
| 3 | 踏みつけ判定は要件の定義どおり「下降中かつ下端が敵の上半分に重なる」 | 前フレームの底面と敵上面を比べる（game-knowledge.md） | 受入条件と判定式が一致し、テストの期待値をそのまま書ける。最大落下速度 240 px/s は 1 フレーム 4 px で、敵の上半分 8 px を飛び越えない |
| 4 | 重力は速度を先に更新し、位置を後に更新する。ジャンプ初速は 345 px/s | 位置を先に更新する。初速 350 px/s（game-knowledge.md の値） | 位置を先に更新すると最高到達点が 69 px で REQ-006 の 62〜66 px を外れる。落下上限も要件の 240 px/s を優先する |
| 5 | 更新は固定 1/60 秒のステップだけにし、実時間はためて消化する。滑走開始からの猶予は整数フレームで数える | 可変 dt をそのまま渡す。猶予を秒の浮動小数で比べる | REQ-101 が固定 60 FPS。受入条件が「12 フレーム」で、浮動小数の丸めによる境界のずれを避けられる |
| 6 | 猶予の境界: `slide_age <= 12` は無害、`slide_age > 12` で死亡 | 境界を決めない | REQ-049「12 フレーム以内は死なない」と REQ-024「12 フレーム経過後は死ぬ」の間に隙間を作らず、テスト仕様で一意にするため |
| 7 | ステージの左右端（col < 0, col >= 200）を壁として扱う。上端の外は空、下端の外も空（穴に落ちる） | 端を特別扱いしない | 端がないとプレイヤーと敵がマップ外へ出る。REQ-009（壁を通り抜けない）の延長で、REQ-030 の落下死は成立したまま |
| 8 | 静止甲羅への接触は上からでも横からでも蹴り出し、跳ね返りはしない。敵を踏んだら、プレイヤーの下端を敵の上面に合わせて重なりを解消してから跳ね返す | 上から踏んだら跳ね返る。重なりを解消せず再接触の猶予時間を設ける | REQ-020 は接触方向を問わない。跳ね返りを足すと REQ-016 と REQ-020 の両方が当たる接触になり、判定が二重になる。踏んだ直後に重なりが残ると、次フレームで静止甲羅が蹴り出されるため、押し上げで重なりそのものをなくす（猶予時間の状態を増やさない） |
| 9 | 敵にも重力と衝突を使う。歩行敵・歩行甲羅は崖で反転し、滑走中の甲羅は崖で反転せず落ちる | 敵は重力なしで y 固定 | 滑走する甲羅が足場の外で宙に浮くのを避ける。崖の反転は REQ-014 が歩行敵だけに求めるため、滑走甲羅は対象外 |
| 10 | プレイヤーと敵が同時に接触するとき、踏みつけを先に処理し、その後に死亡接触を判定する | リスト順に処理する | 敵を踏みながら別の敵に触れても理不尽に死なない。順序が配置に依存しない |
| 11 | キー入力とタッチ入力はどちらも HeldButtons に変換して OR で合わせる | 入力ごとに別の InputState を作る | REQ-045「同じ入力状態になる」を型で保証できる。Game 層はキーコードもタッチも知らない |
| 12 | Web 版は pygbag で作り、`main()` を async にする | ネイティブ iOS アプリ。別の Web 化手段 | 要件で Web ブラウザ版に確定済み。pygbag は pygame-ce を動かせ、iPhone と Mac の両方に同じ成果物で届く |
| 13 | ジャンプのコヨーテタイムとバッファは入れない | game-knowledge.md の定石どおり入れる | REQ-005「空中ではジャンプしない」に反し、要件にない機能になるため（YAGNI） |
| 14 | 内部描画面の拡大は縦横比を保った小数倍にする。倍率は `min(window_w / SCREEN_W, window_h / SCREEN_H)` | 整数倍のみ。整数倍を基本にして足りないときだけ小数倍 | 整数倍では iPhone の横向き（高さ約 375 px）で倍率が 1 に固定され、画面が小さいままになる（人間の指摘）。REQ-102 が小数倍を許可した。倍率の計算は純関数にできテストしやすい |
| 15 | 仮想ボタンとゲーム画面は別領域にする。ステージ領域（上 240 px）への描画はクリップし、下 64 px を操作パネルとして常に描く | ゲーム画面の上にボタンを半透明で重ねる（従来）。タッチ端末でだけ画面を伸ばす | 重ねるとマリオや敵が隠れる（人間の指摘）。端末で画面の構成が変わると、検証が端末ごとになる。常に同じ構成にすれば REQ-055 も満たせ、描画の分岐が減る |
| 16 | 操作パネルは、ステージの地面の続きとして列ごとに描く。最下段が空の列は黒で塗り、プレイヤーと敵はクリップなしで操作パネルの後に描く | 操作パネルを一様な地面で塗る（1 件目の実装）。ステージを 2 段深くして穴を 64 px にする | 一様な地面では穴が 32 px の凹みに見える（人間の指摘）。列ごとの判定は純関数 `column_has_ground` にでき、描画の分岐が 1 つ増えるだけ。ステージの寸法（REQ-043）やステージファイルを変えずに済む。プレイヤーと敵をクリップしないと、穴に落ちる途中で y=240 の線で消えてしまう |

## 8. 注意・リスク（人間への共有事項）
- **小数倍の拡大**: ドットの幅が一部不均一に見えることがある（REQ-102、人間が選択）。
- **カメラの追従位置**: 画面を 592 px にしても CAMERA_FOLLOW_X は 128 px のまま（REQ-039 は変えない）。プレイヤーは画面の左寄りに映り、右の見える範囲が広がる。
- **Python のバージョン**: CLAUDE.md は Python 3.14 だが、pygbag が載せる Python は 3.14 とは限らない。問題が出た時点で調整する（人間の指示）。
- **カメラ左端**: プレイヤーが画面の左端から完全に出ると死亡する（REQ-051、人間の指示で追加）。
- **端末判定**: iPhone で最初のタッチ前に仮想ボタンを出すため、起動時に `navigator.maxTouchPoints` で判定する（DES-014）。タッチ対応のない macOS では出ない。

"""プレイヤーと敵、甲羅と歩行敵の接触の解決。"""

from __future__ import annotations

from dataclasses import dataclass

from src.game.constants import SHELL_GRACE_FRAMES, STOMP_BOUNCE_SPEED, STOMP_ZONE_RATIO
from src.game.enemy import Enemy, EnemyKind, EnemyState, kick_shell, stomp_enemy
from src.game.player import Player


@dataclass(frozen=True)
class PlayerEnemyResult:
    player_died: bool


def _can_be_stomped(player: Player, enemy: Enemy) -> bool:
    """下降中で、敵の上半分に重なっていて、静止甲羅でないとき。"""
    box = enemy.body.box
    player_box = player.body.box
    return (
        player.body.vy > 0
        and enemy.state is not EnemyState.SHELL_IDLE
        and player_box.overlaps(box)
        and player_box.bottom <= box.top + box.h * STOMP_ZONE_RATIO
    )


def _is_deadly_contact(enemy: Enemy) -> bool:
    if enemy.state is EnemyState.WALKING:
        return True
    return (
        enemy.state is EnemyState.SHELL_SLIDING and enemy.slide_age > SHELL_GRACE_FRAMES
    )


def resolve_player_enemies(player: Player, enemies: list[Enemy]) -> PlayerEnemyResult:
    alive = [enemy for enemy in enemies if enemy.alive]
    stomped = [enemy for enemy in alive if _can_be_stomped(player, enemy)]
    for enemy in stomped:
        stomp_enemy(enemy)
    if stomped:
        top = min(enemy.body.box.top for enemy in stomped)
        player.body.box.y = top - player.body.box.h
        player.body.vy = -STOMP_BOUNCE_SPEED
    touching = [
        enemy
        for enemy in alive
        if enemy not in stomped and player.body.box.overlaps(enemy.body.box)
    ]
    for enemy in touching:
        if enemy.state is EnemyState.SHELL_IDLE:
            kick_shell(enemy, player.body.box.center_x)
    return PlayerEnemyResult(
        player_died=any(_is_deadly_contact(enemy) for enemy in touching)
    )


def resolve_shells_vs_walkers(enemies: list[Enemy]) -> None:
    alive = [enemy for enemy in enemies if enemy.alive]
    shells = [enemy for enemy in alive if enemy.state is EnemyState.SHELL_SLIDING]
    walkers = [enemy for enemy in alive if enemy.kind is EnemyKind.WALKER]
    for walker in walkers:
        if any(shell.body.box.overlaps(walker.body.box) for shell in shells):
            walker.alive = False

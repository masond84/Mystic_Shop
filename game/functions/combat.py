from game.world import player as default_player
from npc.enemies import enemies
import random

def engage_battle(enemy_name, player=default_player):
    enemy = enemies[enemy_name]

    print(f"\n⚔️ A {enemy.name} appears! {enemy.description}")
    
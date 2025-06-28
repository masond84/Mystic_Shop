from game.world import player as default_player
from game.npc.enemies import enemies
import random

def engage_battle(enemy_name, player=default_player):
    enemy = enemies[enemy_name]

    print(f"\n⚔️ A {enemy.name} appears! {enemy.description}")
    print(f"{enemy.name} has {enemy.hp} HP\n")

    while enemy.is_alive() and player.hp > 0:
        print(f'Your turn! Choose an action:')
        print("Example: attack(), run()")
        action = input(">>> ").strip().lower()

        if action == "attack()":
            player_damage = random.randint(player.attack - random.randint(2, 4), player.attack + random.randint(2, 4))
            print(f"🗡️ You hit {enemy.name} for {player_damage} damage!")
            enemy.take_damage(player_damage)
            print(f"{enemy.name} has {enemy.hp} HP left.\n")
        elif action == "run()":
            chance_of_escape = random.randint(0, 1) # return a value between 0 and 1
            if chance_of_escape == 1:
                print("🏃 You successfully escaped!")
                return
            elif chance_of_escape == 0:
                print("You failed to escape!\n")
                continue
        else:
            print("⚠️ Invalid action. Try again.\n")
            continue

        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!\n")
            break

        # Enemy attack back
        enemy_damage = enemy.get_attack_damage()
        print(f"💥 {enemy.name} hits you for {enemy_damage} damage!\n")
        player.hp = max(0, player.hp - enemy_damage)
        
        if player.hp <= 0:
            print("💀 You have been defeated! Game Over.\n")
            break


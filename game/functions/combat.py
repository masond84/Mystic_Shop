from game.world import player as default_player
from game.npc.enemies import enemies
from game.tutorials import contextual_feedback
import random

def render_health_bar(current_hp, max_hp, bar_length=20):
    ratio = current_hp / max_hp
    filled_length = int(ratio * bar_length)
    empty_length = bar_length - filled_length

    bar = "█" * filled_length + "-" * empty_length
    return f"[{bar}] {current_hp}/{max_hp}"

def color_text(text, color="default"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "default": "\033[0m"
    }
    return f"{colors[color]}{text}\033[0m"


def engage_battle(enemy, player=default_player):

    print(f"\n⚔️ A {enemy.name} appears! {enemy.description}")

    while enemy.is_alive() and player.hp > 0:
        print("🛡️ Battle Status:")
        print(f"{player.name}'s HP:   {color_text(render_health_bar(player.hp, 115), 'green')} {player.hp}/115")
        print(f"{enemy.name}'s HP: {color_text(render_health_bar(enemy.hp, enemy.max_hp), 'red')} {enemy.hp}/{enemy.max_hp}\n")

        # Prompt Player Action
        print(f'Your turn! Choose an action:')
        print("Example: attack(), run(), inventory.show()")
        action = input(">>> ").strip().lower()

        if contextual_feedback(action, player):
            continue

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
            return # ensure you return to explore_area() and prompt the user to continue exploring

        # Enemy attack back
        enemy_damage = enemy.get_attack_damage()
        print(f"💥 {enemy.name} hits you for {enemy_damage} damage!\n")
        player.hp = max(0, player.hp - enemy_damage)
        
        if player.hp <= 0:
            print("💀 You have been defeated! Game Over.\n")
            return


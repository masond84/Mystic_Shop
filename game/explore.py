from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from game.world import items as all_items

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Possible random encounters
encounters = [
    {"type": "item", "description": "You found a shimmering {item}!", "effect": "add_item"},
    {"type": "enemy", "description": "You encountered a wild {enemy}!", "effect": "battle"},
    {"type": "event", "description": "You stumbled into a {event}!", "effect": "event"},
]

# event pools
events = ["mystic fog", "ancient ruin", "strange portal"]

### HELPER FUNCTIONS ###
def build_explore_prompt(encounter_type, item=None, enemy=None, event=None):
    base = (
        "You're a narrator in a fantasy RPG."
        "Write a short and complete 2-sentence description for a player exploring a mystical world."
        "Write a description of the encounter based on encounter type."
        "If the user encounter's an item give an adjective to the item and explain how the player found it."
        "If the user encounter's a enemy, give a description of the enemy and the setting the user encountered it in."
        "If the user encounter's an event mysticly describe the event."
        "End your description with a period."
    )

    if encounter_type == "item":
        item_prompt = f"The player finds a item: {item}"
        settings = ""
        actions = ""
        return base + item_prompt 
    elif encounter_type == "enemy" and enemy:
        enemy_prompt = f"While exploring the player encounters a hostile creature: {enemy}"
        settings = ""
        actions = ""
        return base + enemy_prompt + f" Enemy: {enemy.name}, Description: {enemy.description}"
    elif encounter_type == "event":
        event_prompt = f"The player enters a strange event: {event}"
        settings = ""
        actions = ""
        return base + event_prompt

def generate_encounter_description(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a creative RPG storyteller."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip() 
    except Exception as e:
        return f"[Error generating description: {e}]"

# Function to handle Item Encounters
def handle_item_encounter(item):
    from game.world import player, ingredient_items, regular_items, crafted_items
    from game.tutorials import contextual_feedback

    print(f"\nYou seemed to have found an item: {item}")
    print("What would you like to do?")
    print("- You can add items to your ingredient bag or inventory - or leave it.")
    print("Type `hint()` for help.")

    while True:
        user_input = input(">>> ").strip().lower()

        if user_input in ["leave()", "leave", "skip()"]:
            print(f"🚶 You leave the {item} behind.")
            break
        elif user_input == "hint()":
            if item in ingredient_items:
                print(f"💡 Try: ingredient_bag.add('{item}')")
            elif item in regular_items or item in crafted_items:
                print(f"💡 Try: inventory.update('{{'{item}': 1}}')")
            else:
                print("This item is unknown. Maybe inspect it or leave it.")
        elif "ingredient_bag.add" in user_input or "inventory.update" in user_input:
            contextual_feedback(user_input, player, expected_item=item)
            if item in player.ingredient_bag or item in player.inventory:
                break # Exit after sueccessful add
        elif user_input == "examine()":
            from game.tutorials import examine_item 
            examine_item(item)
        else:
            print("⚠️ Unknown command. Try again or type `leave()` or 'hint()'")

def explore_area():
    print("\n🧭 Entering Exploration Mode! Type 'menu' to return to main menu.\n")

    while True:
        encounter = random.choice(encounters)
        encounter = encounters[0] # For testing, force item encounter

        # Generate a random occurencce
        if encounter["type"] == "item":
            item = random.choice(list(all_items))
            prompt = build_explore_prompt("item", item=item)
            description = generate_encounter_description(prompt)
            print(description)
            handle_item_encounter(item)

        elif encounter["type"] == "enemy":
            from game.npc.enemies import enemies as enemy_dict
            enemy_factor = random.choice(list(enemy_dict.values()))
            enemy = enemy_factor()

            prompt = build_explore_prompt("enemy", enemy=enemy)
            description = generate_encounter_description(prompt)
            
            print(description)

            # Placeholder to later integrate battle system
            from game.functions.combat import engage_battle
            engage_battle(enemy)
        
        elif encounter["type"] == "event":
            event = random.choice(events)
            prompt = build_explore_prompt("event", event=event)
            description = generate_encounter_description(prompt)
            print(description)
            print(f"An event occured: {event}")

            # Placeholder: Unique event logic
        
        while True:
            proceed = input("\n🌿 Would you like to continue exploring?" + " (yes/no):\n" + ">>> ").strip().lower()
            if proceed in ("yes", "y"):
                break
            elif proceed in ("no", "n", "menu", "exit", "return"):
                print("📜 Returning to main menu...\n")
                return
            else:
                print("Please enter 'yes' or 'no'.")
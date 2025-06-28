from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from game.world import player, items as all_items, all_recipes
from game.tutorials import contextual_feedback

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Possible random encounters
encounters = [
    {"type": "item", "description": "You found a shimmering {item}!", "effect": "add_item"},
    {"type": "enemy", "description": "You encountered a wild {enemy}!", "effect": "battle"},
    {"type": "event", "description": "You stumbled into a {event}!", "effect": "event"},
]

# Enemy and event pools
enemies = ["goblin", "dragon", "bandit", "slime"]
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
    elif encounter_type == "enemy":
        enemy_prompt = f"While exploring the player encounters a hostile creature: {enemy}"
        settings = ""
        actions = ""
        return base + enemy_prompt
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

def explore_area():
    print("\n🧭 Entering Exploration Mode! Type 'menu' to return to main menu.\n")

    while True:
        encounter = random.choice(encounters)
        encounter = encounters[1]
        description = ""

        # Generate a random occurencce
        if encounter["type"] == "item":
            item = random.choice(list(all_items))
            prompt = build_explore_prompt("item", item=item)
            description = generate_encounter_description(prompt)
            print(description)
            print(f"You seemed to find an item: {item}")

            # Prompt For Player Input on What To Do
            while True:
                print("What would you like to do?")
                print("You can add items to your ingredient bag or inventory - or leave it.")
                action = input(">>> ").strip().lower()

                if action in ("leave", "back"):
                    print("You leave the item and move on.\n")
                    break
                elif action == "menu":
                    from game.engine import start_game
                    start_game()
                elif "ingredient_bag" in action or "inventory.update" in action:
                    from game.tutorials import contextual_feedback
                    contextual_feedback(action)
                    break
                elif action.lower() == "examine":
                    from game.tutorials import examine_item
                    examine_item(item)
                else:
                    print("⚠️ Unknown command. Try again or type 'leave' to exit")
        elif encounter["type"] == "enemy":
            enemy = random.choice(enemies)
            prompt = build_explore_prompt("enemy", enemy=enemy)
            description = generate_encounter_description(prompt)
            print(description)
            print(f"You encountered a enemey: {enemy}")

            # Placeholder to later integrate battle system
        elif encounter["type"] == "event":
            event = random.choice(events)
            prompt = build_explore_prompt("event", event=event)
            description = generate_encounter_description(prompt)
            print(description)
            print(f"An event occured: {event}")

            # Placeholder: Unique event logic
        
        # Handle user input inside explore mode
        user_input = input(">>> ").strip().lower()
        if user_input in ("menu", "exit", "return"):
            print("Returning to the main menu...\n")
            break
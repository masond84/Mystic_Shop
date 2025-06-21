# game/tutorials.py
from game.world import player as default_player
from game.world import all_recipes
from game.world import items as all_items
from game.world import ingredient_items, crafted_items, regular_items
import re

# Tutorial state
completed_tasks = set()
required_ingredients = all_recipes["potion"]
tutorial_phase = "gathering"

# Tutorial Steps
steps =  {
    "gather_ingredients": required_ingredients,
    "learn_recipe": "recipes.get('potion')",
    "craft_potion": "inventory.update({'potion': 1})"
}

# -------------------------------
# 🧠 Canonical Known Items & Normalizer
# -------------------------------
known_items = set(all_items)
known_recipes = set(all_recipes.keys())

# Create mapping for underscores/spaces
normalized_map = {item.replace(" ", "_"): item for item in known_items}
normalized_map.update({item.replace("_", " "): item for item in known_items})


# Util function
def extract_clean_item(input_text: str) -> str:
    """
    Extract and normalize an item from a user command input.
    E.g. "ingredient_bag.add('unicorn_hair')" → "unicorn hair"
    """
    match = re.search(r"\(\s*['\"](.+?)['\"]\s*\)", input_text)
    raw_item = match.group(1).strip() if match else ""
    normalized = raw_item.replace("_", " ").lower()

    # Match against known items (case-insensitive)
    for canonical in known_items:
        if normalized == canonical.lower():
            return canonical
    if normalized in normalized_map:
        return normalized_map[normalized]

    return raw_item  # fallback (used for warning)

def show_intro():
    global tutorial_phase
    
    # CHECK IF USER HAS COMPLETED INTRO
    if tutorial_phase == "gathering":
        print("""
        Welcome, apprentice. Your journey to become a master alchemist begins here.
        
            In this game, you'll master:
            - set.add(), set.remove(), set.issubset(), set.union()
            - dict.get(), dict.keys(), dict.values(), dict.items(), dict.update()
            - for loops over dictionaries and sets
        
        📜 First task:
            Use `ingredient_bag.add('<ingredient_name>')` to collect the following:
            - unicorn hair
            - phoenix feather
            - elixr of life
        """)

def check_task_completion(user_input, player=default_player):
    global tutorial_phase

    if tutorial_phase == "gathering":
        if required_ingredients.issubset(player.ingredient_bag):
            print("\n🎉 Congratulations! You've collected all the required ingredients with sets.")
            tutorial_phase = "learn_recipe"
            print("\n📜 Next task: Learn the potion recipe.")
            print("Use: recipes.get('potion') to learn the potion recipe.")
            print("Or try, for recipe, ingredient in recipes.items(): print(recipe, ingredient)")
        else:
            missing = required_ingredients - player.ingredient_bag
            print(f"\n⚠️ You still need to collect: {', '.join(missing)}")
    elif tutorial_phase == "learn_recipe":
        if "potion" in player.learned_recipes:
            print("\n🎉 You've learned how to read the recipes with sets!")
            tutorial_phase = "crafting"
            print("\n📜 Next task: Craft a potion using the ingredients.")
            print("Use: inventory.update({'potion': 1}) to craft a potion.")
            print("Or try, for item in inventory.keys(): print(item)")
        else:
            print("\n📖 Try using the correct function to craft")
    elif tutorial_phase == "crafting":
        if user_input.strip() == steps["craft_potion"]:
            print("🎉 You've successfully learned to craft with dictionaries!")
            tutorial_phase = "completed"
            print("Tutorial completed! You are now ready to explore the world.")
        else:
            print("Try: inventory.update()")
    elif tutorial_phase == "use_potion":
        if user_input.strip() == "completed":
            if "elixer of life" not in player.inventory:
                print("You need to craft the potion first!")
            else:
                print("You used the elxir and completed the tutorial🧙")
                tutorial_phase = "completed"
        else:
            print("💡Try using `ingredient_bag.remove('elixir of life')`")
    elif tutorial_phase == "completed":
        print("You have completed the tutorial! You can now explore the world and continue your adventure.")     
        print("Type 'menu' to return to the main menu or 'exit' to quit.")

def contextual_feedback(user_input, player=default_player):
    item = extract_clean_item(user_input)

    is_valid_item = item in all_items
    is_valid_recipe = item in player.learned_recipes
    
    ### INGREDIENT BAG MANAGEMENT ###
    # Player adds an item to the ingredient bag set
    # Players can only cary one of each ingredient
    if user_input.startswith("ingredient_bag.add("):
        if not is_valid_item:
            print(f"❌ '{item}' is not a valid in-game item. Please check your spelling.")
            return
        
        if item not in known_items:
            print(f"⚠️ '{item}' is not recognized. Ignoring.")
            return
        
        if item not in ingredient_items:
            print(f"❌ `{item}` cannot go in the ingredient bag. It's not a valid ingredient.")
            print("💡 Only one of each raw crafting ingredients can go in the ingredient bag.")
            return
    
        if item in player.ingredient_bag:
            print(f"⚠️ '{item}' is already in your ingredient bag.")
            return

        player.add_ingredient(item)
        player.show_ingredient_bag()
    # Player removes an item from the ingredient bag set
    elif user_input.startswith("ingredient_bag.remove("):
        try:
            item = extract_clean_item(user_input)
            if item in player.ingredient_bag:
                player.ingredient_bag.remove(item)
                print(f"🎒 You used: {item}")
                player.show_ingredient_bag()
            else:
                print(f"⚠️ {item} is not in your ingredient bag.")
        except Exception as e:
            print(f"Error removing ingredient: {e}")
    elif "for item in ingredient_bag" in user_input and "print(item)" in user_input:
        player.show_ingredient_bag()
    ### INVENTORY MANAGEMENT ###
    # Player adds an item to the inventory backpack dictionary
    elif user_input.startswith("inventory.update("):
        match = re.search(r"update\(\{\s*['\"](.+?)['\"]\s*:\s*(\d+)\s*\}\)", user_input)
        if match:
            item_name = match.group(1).strip()
            count = int(match.group(2))

            if item_name not in crafted_items and item_name not in regular_items:
                print(f"❌ '{item_name}' cannot be added to inventory directly. It must be crafted or discovered.")
                print("💡 Only crafted or discoverable items go in your inventory.")
                return 
            
            success = player.craft_item(item_name)
            if success:
                player.show_inventory()
        else:
            print("⚠️ Invalid syntax. Try: inventory.update({'potion': 1})")
    # Player checks items in their inventory backpack dictionary
    elif user_input.startswith("inventory.keys("):
        if player.inventory:
            player.show_inventory()
        else:
            print("\n🎒 Inventory:")
            print("...")
            print("Your inventory is empty")
    ### RECIPE MANAGEMENT ###
    elif user_input.strip().startswith("recipes.get("):
        match = re.search(r"recipes\.get\(['\"](.+?)['\"]\)", user_input)
        if match:
            recipe_name = match.group(1).strip()
            if recipe_name in all_recipes:
                player.learn_recipe(recipe_name)
    elif re.match(r"^for\s+\w+,\s*\w+\s+in\s+recipes\.items\(\):", user_input.strip()):
        player.show_learned_recipes()
                
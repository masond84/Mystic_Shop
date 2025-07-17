# game/world.py
import re

# Global dictionary of all recipes in the game
all_recipes = {
    "potion": {"unicorn hair", "phoenix feather", "elixir of life"},
    "magic sword": {"dragon scale", "mithril"},
    "elixir of fire": {"lava droplet", "fire flower", "dragon scale"}
}
# Global set to store all items in game
items = {
    "elixir of life",
    "unicorn hair",
    "phoenix feather",
    "dragon scale",
    "mithril",
    "lava droplet",
    "fire flower",
    "magic sword",
    "potion",
    "elixir of fire",
}
# Gloabl ingredient items
ingredient_items = {
    "unicorn hair",
    "phoenix feather",
    "dragon scale",
    "fire flower",
    "lava droplet",
    "mithril"
}
# Global craftable items
crafted_items = set(all_recipes.keys())
# Global regular items
regular_items = items - ingredient_items - crafted_items

# ALL Biomes
biomes = ["forest", "desert", "mountain", "swamp", "cave", "plains"]

# Item Effects
item_effects = {
    "potion": {"hp": 30},
    "elixir of fire": {"attack": 3}, # boosts attack power by 3 temporarily
    "elixir of life": {"hp": 50},
}

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 115
        self.max_hp = 115
        self.level = 1
        self.attack = 5 # initial attack power
        self.defense = 5
        self.ingredient_bag = set()
        self.inventory = {}
        self.learned_recipes = set()
        self.orders = {}
    
    @property
    def recipe_dict(self):
        return {name: all_recipes[name] for name in self.learned_recipes}

    ### INGREDIENT BAG MANAGEMENT ###
    def show_ingredient_bag(self, command=None):
        if not command:
            print("🎒 Ingredient Bag:")
            if self.ingredient_bag:
                for item in sorted(self.ingredient_bag):
                    print(f"↪ {item}")
            else:
                print("💨 Your ingredient bag is empty.")
            print()
            return True
        
        # Match patterns like: for x in ingredient_bag: print(x)
        match_single = re.match(r"for\s+(\w+)\s+in\s+ingredient_bag\s*:\s*print\(\s*\1\s*\)", command)
        if match_single:
            print("🎒 Ingredient Bag:")
            if self.ingredient_bag:
                for item in sorted(self.ingredient_bag):
                    print(item)
            else:
                print("💨 Your ingredient bag is empty.")
            return True
        
        return False
    
    # Player removes an ingredient from the ingredient bag set
    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredient_bag and ingredient in items:
            self.ingredient_bag.remove(ingredient)
            print(f"✅ Removed {ingredient} from your ingredient bag.")
    # Player adds an ingredient to the ingredient bag set
    def add_ingredient(self, ingredient):
        if ingredient not in items:
            print(f"❌ {ingredient} is not a valid ingredient.")
            return
        elif ingredient in items and ingredient not in self.ingredient_bag:
            self.ingredient_bag.add(ingredient)
            print(f"📦 Added {ingredient} to your ingredient bag.")
        else:
            print(f"❌ {ingredient} is not a valid ingredient.")

    ### INVENTORY MANAGEMENT ###
    # Player adds an item to the inventory backpack dictionary
    def add_to_inventory(self, item, quantity=1):
        if item not in items:
            print(f"{item} is not a valid item.")
            return
        
        # If item in inventory, increase quantity
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        print(f"🎒 You added {quantity} {item}(s) to your inventory.")

    # Display items in inventory - take in optional command allowing for printing dictionary in different formats
    def show_inventory(self, command=None, suggest_usage=False):
        """
        Display inventory and optionally let player interact with items after viewing.
        """
        def post_inventory_actions():
            """Inner helper loop for interacting with items."""
            next_action = input(
                "\n✨ Would you like to interact with an item? "
                "(use_item('<item>'), cheat_add_items({...}), or 'back')\n>>> "
            ).strip().lower()

            if next_action.startswith("use_item(") or next_action.startswith("cheat_add_items("):
                from game.tutorials import contextual_feedback
                contextual_feedback(next_action, self)
            elif next_action in ("back", "no", "exit"):
                print("↩️ Returning to gameplay...")
            else:
                print("Unknown command. Try use_item(`<item>`) or type 'back' to return.")

        # --- DEFAULT INVENTORY DISPLAY ---
        if not command:
            print("🎒 Inventory:")
            if self.inventory:
                for item, quantity in sorted(self.inventory.items()):
                    print(f"↪ {item}: {quantity}")
                if suggest_usage:
                    print("\n💡 Type use_item('<item>') to consume something.")
                    post_inventory_actions()
            else:
                print("💨 Your inventory is empty.")
            return True
        
        # Match patterns like: for x in inventory: print(x)
        match_items = re.match(r"for\s+(\w+)\s+in\s+inventory\s*:\s*print\(\s*\1\s*\)", command)
        if match_items:
            print("🎒 Inventory:")
            if self.inventory:
                for item in sorted(self.inventory.keys()):
                    print(item)
                if suggest_usage:
                    print("\n💡 Type use_item('<item>') to consume something.")
                    post_inventory_actions()
            else:
                print("💨 Your inventory is empty.")
            return True
        
        # Match patterns like: for a, b in inventory.items(): print(a, b)
        match_pairs = re.match(r"for\s+(\w+)\s*,\s*(\w+)\s+in\s+inventory\.items\(\)\s*:\s*print\(\s*\1\s*,\s*\2\s*\)", command)
        if match_pairs:
            print("🎒 Inventory:")
            if self.inventory:
                for item, quantity in self.inventory.items():
                    print(f"{item} {quantity}")
                if suggest_usage:
                    print("\n💡 Type use_item('<item>') to consume something.")
                    post_inventory_actions()
            else:
                print("💨 Your inventory is empty.")
            return True
        
        return False
    
    ### RECIPE MANAGEMENT ###
    def learn_recipe(self, recipe_name):
        if recipe_name in self.learned_recipes:
            print("📖 You already know the {recipe_name} recipe.")
            return
        
        if recipe_name in all_recipes:
            self.learned_recipes.add(recipe_name)
            print(f"⚡ You have learned the {recipe_name} recipe!")
        else:
            print(f"{recipe_name} is not a valid recipe.")

    def show_learned_recipes(self):
        print("\n📖 Learned Recipes:")
        if self.learned_recipes:
            for recipe in sorted(self.learned_recipes):
                ingredients = ", ".join(all_recipes.get(recipe, []))
                print(f"↪ {recipe}: {ingredients}")
        else:
            print("You haven't learned any recipes yet.")
        print()

    ### CRAFTING MANAGEMENT ###
    # Allow players to craft items and add them to inventory backpack dictionary
    def craft_item(self,item_name):
        if item_name not in self.learned_recipes:
            print(f"📖 You haven't learned the recipe for {item_name} yet.")
            return False

        required_ingredients = all_recipes.get(item_name, set())

        if not required_ingredients.issubset(self.ingredient_bag):
            missing = required_ingredients - self.ingredient_bag
            print(f"❌ You don't have the required ingredients to craft {item_name}. Missing: {', '.join(missing)}")
            return False
        # Remove ingredients from ingredient bag
        for ingredient in required_ingredients:
            self.ingredient_bag.remove(ingredient)

        # Add item to inventory
        self.add_to_inventory(item_name)
        print(f"🛠️ You have successfully crafted: {item_name}")
        return True
    
    ### Player Actions ###
    # use item
    def use_item(self, item_name):
        from game.world import item_effects

        if item_name not in self.inventory or self.inventory[item_name] <= 0:
            print(f"❌ You don't have {item_name} in your inventory.")
            return False
        if item_name not in item_effects:
            print(f"❌ {item_name} has no effect.")
            return False
        
        effects = item_effects[item_name]
        print(f"✨ Using {item_name}...")

        if "hp" in effects:
            healed = min(self.max_hp - self.hp, effects["hp"])
            self.hp += healed
            print(f"❤️ You healed {healed} HP. Current HP: {self.hp}/{self.max_hp}")
        if "attack" in effects:
            self.attack += effects["attack"]
            print(f"⚔️ Your attack power increased by {effects['attack']}! Current Attack: {self.attack}")

        # Decrement item count
        self.inventory[item_name] -= 1
        if self.inventory[item_name] <= 0:
            del self.inventory[item_name]
        
        return True
    
    ## CHEAT CODES ##
    def cheat_add_items(self, items_to_add):
        """
        Quickly add items to inventory for testing.
        Example: cheat_add_items({'potion': 5, 'elixir of life': 2})
        """
        for item, qty in items_to_add.items():
            if item in items:
                self.add_to_inventory(item, quantity=qty)
            else:
                print(f"❌ {item} is not a recognized item.")

# Create a player instance
player = Player("Hero")
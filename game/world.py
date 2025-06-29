# game/world.py

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
ingredient_items = {ingredient for recipe in all_recipes.values() for ingredient in recipe}
# Global craftable items
crafted_items = set(all_recipes.keys())
# Global regular items
regular_items = items - ingredient_items - crafted_items

# ALL Biomes
biomes = ["forest", "desert", "mountain", "swamp", "cave", "plains"]

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
    def show_ingredient_bag(self):
        print("\n🎒 Ingredient Bag:")
        if self.ingredient_bag:
            for item in sorted(self.ingredient_bag):
                print(f"- {item}")
        else:
            print("Your ingredient bag is empty.")
        print()

    def remove_ingredient(self, ingredient):
        if ingredient in self.ingredient_bag and ingredient in items:
            self.ingredient_bag.remove(ingredient)
            print(f"✅ Removed {ingredient} from your ingredient bag.")
    
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

    def show_inventory(self):
        print("\n🎒 Inventory:")
        if self.inventory:
            for item, quantity in sorted(self.inventory.items()):
                print(f"↪ {item}: {quantity}")

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


# Create a player instance
player = Player("Hero")
# game/engine.py
# Allows users to type things to interact with the game like
# adding ingredients, crafting items, and fulfilling orders.
# ingredient_bag.add('unicorn_hair')
# "potion" in recipes
# "magic sword" in inventory
from game.explore import explore_area
from game.world import player, all_recipes
from game import tutorials

def start_game():
    while True:
        show_main_menu()
        user_input = input(">>> ")
        
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Thanks for playing! Goodbye.")
            break
        
        if user_input == "1":
            print("Exploring...")
            explore_area()
        elif user_input == "2":
            print("Crafting items... (feature not implemented yet)")
        elif user_input == "3":
            print("Selling items... (feature not implemented yet)")
        elif user_input == "4":
            print("Buying items... (feature not implemented yet)")
        elif user_input == "5":
            tutorial_loop()
        else:
            print("Invalid choice. Please try again.")
            
def show_main_menu():
    print("\n🧙 Welcome to the Mystic Shop!")
    print("What would you like to do?")
    print("1. Explore")
    print("2. Craft")
    print("3. Sell")
    print("4. Buy")
    print("5. Tutorial")
    print("Type the number of your choice or 'exit' to quit.")

def tutorial_loop():
    tutorials.show_intro()
    while True:
        user_input = input(">>> ")

        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Exiting tutorial. Returning to main menu.")
            break
        
        if user_input.strip().lower() == "menu":
            print("Returning to main menu...")
            start_game()
        
        try:
            # Execute the user's input as Python code
            '''
            exec(user_input, globals(), {
                "ingredient_bag": player.ingredient_bag,
                "inventory": player.inventory,
                "recipes": player.recipes,
                "orders": player.orders,
                "tutorials": tutorials,
            })
            '''

            # Show contextual feedback based on what they typed
            tutorials.contextual_feedback(user_input, player)

            # Check if the task is completed
            tutorials.check_task_completion(user_input, player)
        except Exception as e:
            print(f"Error: {e}")

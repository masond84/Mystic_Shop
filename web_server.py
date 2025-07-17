from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from game.tutorials import contextual_feedback
from game.world import player
from game.engine import start_game_web, tutorial_loop
from game.web_output import get_history, append_output
import sys
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

class Command(BaseModel):
    input: str

# call once when server starts to initalize main menu
start_game_web()

# store output history
# output_history = ["🧙 Welcome to Mystic Shop! Type a command below:"]

# Call once when server starts to initialize main menu
start_game_web()

@app.post("/command")
def send_command(cmd: Command):
    user_input = cmd.input.strip().lower()
    append_output(f">>> {user_input}")

    # Redirect print() to capture output
    buffer = io.StringIO()
    sys_stdout_original = sys.stdout
    sys.stdout = buffer

    try:
        # Handle main menu commands like start_game() does
        if user_input in ["1", "explore()"]:
            from game.explore import explore_area
            explore_area()
        elif user_input == "2":
            print("🛠️ Crafting items... (feature not implemented yet)")
        elif user_input == "3":
            print("💰 Selling items... (feature not implemented yet)")
        elif user_input == "4":
            print("🛒 Buying items... (feature not implemented yet)")
        elif user_input in ["5", "tutorial()"]:
            from game.engine import tutorial_loop
            tutorial_loop()
        elif user_input in ["exit", "quit", "stop"]:
            print("👋 Thanks for playing! Goodbye.")
        else:
            from game.tutorials import contextual_feedback
            contextual_feedback(user_input, player)
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Restore original stdout
        sys.stdout = sys_stdout_original

    # Add captured print output to history
    captured_output = buffer.getvalue()
    if captured_output.strip():
        for line in captured_output.strip().splitlines():
            append_output(line)
            
    return {"output": get_history()}

@app.get("/history")
def get_history():
    """Return the full game history for frontend display"""
    return {"output": get_history()}
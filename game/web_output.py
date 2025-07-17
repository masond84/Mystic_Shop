# game/web_output.py
output_history = []

def append_output(text):
    output_history.append(text)

def get_history():
    return "\n".join(output_history)
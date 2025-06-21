# 🧙 Mystic Shop

Mystic Shop is a text-based Python RPG that teaches players how to use `set` and `dict` operations interactively. Explore, gather ingredients, craft magical items, and face random encounters in a fantasy world!

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key (for dynamic storytelling)

### Setup Instructions

1. **Clone the repo**:
```bash
   git clone https://github.com/YOUR_USERNAME/mystic-shop.git
   cd mystic-shop
```

Install dependencies
```bash
pip install -r requirements.txt
```

Set your OpenAI API key:
Create a .env file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Run the game
```bash
python main.py
```

---
## How to Play
🧙 Welcome to the Mystic Shop!
What would you like to do?
1. Explore
2. Craft
3. Sell
4. Buy
5. Tutorial

### 🧪 Tutorial Mode
Collect ingredients with:
```bash
ingredient_bag.add('unicorn hair')
```

Learn recipes with:
```bash
recipes.get('potion')
```

Craft items using:
```bash
inventory.update({'potion': 1})
```

🌲 Exploration Mode
- Type 1 to Explore.
- Encounter items, enemies, or events.

When finding items, choose to:
- Add to your ingredient_bag
- Examine the item
- Ignore it

---
## Project Structure
```css
mystic-shop/
├── game/
│   ├── engine.py
│   ├── explore.py
│   ├── tutorials.py
│   └── world.py
├── main.py
├── requirements.txt
└── README.md
```

---
## Features
- Interactive command input using python code
- Dynamic GPT-4 storytelling during exploration
- Ingredient vs. crafted item logic enforcement
- Expanding exploration, enemies, and crafting

---
## Future Plans
- Battle system
- Shop & economy
- Inventory weight limits
- Save/load progress
- Web-based UI with Flask or React

---
## Implementation
```yaml
---

## ✅ STEP 4: Commit and Push the README

After adding `README.md`:

```bash
git add README.md
git commit -m "Add README with setup and gameplay instructions"
git push

```
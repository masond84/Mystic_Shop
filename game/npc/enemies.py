from game.world import biomes
import random


class Enemy:
    def __init__(self, name, hp, attack, defense, description=""):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.description = description

    def is_alive(self):
        # Return True if the enemy's HP is greater than 0
        return self.hp > 0

    def take_damage(self, damage):
        # Reduce the enemy's HP by the damage amount 
        self.hp = max(0, self.hp - damage)
    
    def get_attack_damage(self):
        # Calculate damage dealt by the enemy
        return random.randint(self.attack - 2, self.attack + 2)


# NPC ENEMIES
enemies = {
    "goblin": lambda: Enemy("Goblin", hp=20, attack=5, defense=2, description=f"A sneaky {random.choice(biomes)} goblin."),
    "dragon": lambda: Enemy("Dragon", hp=100, attack=20, defense=10, description=f"A fearsome {random.choice(biomes)} dragon."),
    "slime": lambda: Enemy("Slime", hp=15, attack=3, defense=1, description=f"A bouncy {random.choice(biomes)} slime."),
}
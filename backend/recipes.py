
from typing import List

class Recipe:
    def __init__(self, name: str, instructions: List[str]):
        self.name = name
        self.instructions = instructions

def hard_coded_recipes() -> List[Recipe]:
    return [
        Recipe("Pancakes", [
            "Mix flour, milk, eggs, and sugar in a bowl.",
            "Heat a skillet and add butter.",
            "Pour batter onto the skillet and cook until bubbles form.",
            "Flip the pancake and cook until golden brown."
        ]),
        Recipe("Scrambled Eggs", [
            "Crack eggs into a bowl and whisk them.",
            "Heat a pan and add butter.",
            "Pour the eggs into the pan and stir gently.",
            "Cook until the eggs are just set."
        ]),
        Recipe("Vegetable Stir Fry", [
            "Chop vegetables like bell peppers, broccoli, and carrots.",
            "Heat oil in a pan.",
            "Add vegetables and stir fry until tender.",
            "Season with soy sauce and serve."
        ])
    ]

def print_recipe(recipe: Recipe):
    print(f"Recipe: {recipe.name}")
    for step in recipe.instructions:
        print(f"- {step}")
recipes = hard_coded_recipes()
print_recipe(recipes[0])  
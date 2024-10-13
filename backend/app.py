import os
import sys
import ollama
import cv2
import time
import re
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['APP_NAME'] = 'SousChef API'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Recipe instructions
omelette_instructions = [
    {"instruction": "Crack 2-3 eggs into a bowl."},
    {"instruction": "Whisk the eggs until well beaten."},
    {"instruction": "Add a pinch of salt and pepper to the eggs."},
    {"instruction": "Heat a non-stick pan over medium heat."},
    {"instruction": "Add a small amount of butter or oil to the pan."},
    {"instruction": "Pour the egg mixture into the pan."},
    {"instruction": "Cook until the edges start to set (about 2 minutes)."},
    {"instruction": "Add your chosen fillings to one half of the omelette."},
    {"instruction": "Fold the other half of the omelette over the fillings."},
    {"instruction": "Cook for another minute until the cheese melts (if used)."},
    {"instruction": "Slide the omelette onto a plate."}
]

pancake_instructions = [
    {"instruction": "In a bowl, mix 1 cup of flour, 2 tablespoons of sugar, 2 teaspoons of baking powder, and a pinch of salt."},
    {"instruction": "In another bowl, whisk 1 cup of milk, 1 egg, and 2 tablespoons of melted butter."},
    {"instruction": "Combine the wet ingredients with the dry ingredients and mix until just combined."},
    {"instruction": "Heat a non-stick pan over medium heat."},
    {"instruction": "Pour 1/4 cup of batter for each pancake onto the pan."},
    {"instruction": "Cook until bubbles form on the surface (about 2-3 minutes)."},
    {"instruction": "Flip the pancake and cook for another 1-2 minutes until golden brown."},
    {"instruction": "Repeat with the remaining batter."},
    {"instruction": "Serve with your favorite toppings like syrup or fruit."}
]

quesadilla_instructions = [
    {"instruction": "Heat a non-stick skillet over medium heat."},
    {"instruction": "Place one tortilla in the skillet."},
    {"instruction": "Sprinkle cheese and your choice of fillings (like chicken, beans, or vegetables) on half of the tortilla."},
    {"instruction": "Fold the tortilla in half over the fillings."},
    {"instruction": "Cook until the tortilla is golden brown and the cheese is melted (about 2-3 minutes per side)."},
    {"instruction": "Remove from the skillet and let it cool for a minute."},
    {"instruction": "Cut into wedges and serve with salsa or sour cream."}
]

recipes = {
    "omelette": omelette_instructions,
    "pancakes": pancake_instructions,
    "quesadillas": quesadilla_instructions
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    """
    Custom implementation to sanitize filenames
    """
    filename = re.sub(r'[^\w\.\-]', '', filename)
    filename = re.sub(r'\.+', '.', filename)
    return filename.strip('.')

def get_image_description(image_path):
    """Get a description of the image from the API."""
    res = ollama.chat(
        model="llava:13b",
        messages=[
            {
                "role": "user",
                "content": f"Describe the contents of the image, focusing on the cooking activity and ingredients visible.",
                "images": [image_path]
            }
        ]
    )
    return res["message"]["content"]

def extract_keywords(instruction_text):
    """Extract relevant keywords from the instruction text."""
    keywords = []
    if "whisk" in instruction_text.lower():
        keywords.extend(["whisk", "eggs"])
    elif "crack" in instruction_text.lower():
        keywords.extend(["crack", "eggs"])
    elif "fold" in instruction_text.lower():
        keywords.extend(["fold", "tortilla", "fillings"])
    elif "cook" in instruction_text.lower():
        keywords.extend(["cook", "heat", "pan", "golden brown"])
    return keywords

def compare_image_with_instruction(user_image_path, instruction_text):
    """Compare the user's cooking image with the instruction."""
    user_image_description = get_image_description(user_image_path)
    keywords = extract_keywords(instruction_text)

    contains_keywords = any(keyword in user_image_description.lower() for keyword in keywords)

    res = ollama.chat(
        model="llava:13b",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Does the image show the correct cooking step being performed? "
                    f"Focus on the main activity and any ingredients that should be visible. "
                    f"Instruction: {instruction_text} "
                    f"Image Description: {user_image_description}"
                )
            }
        ]
    )

    ai_feedback = res["message"]["content"]
    
    if "yes" in ai_feedback.lower() or contains_keywords:
        result = "YES"
        feedback = "The step appears to be performed correctly based on the image."
    else:
        result = "NO"
        feedback = "The step was not completed correctly. Please check the instruction again."

    return user_image_description, result, feedback

@app.route('/')
def home():
    return jsonify({
        "name": app.config['APP_NAME'],
        "description": "A virtual cooking assistant API",
        "version": "1.0.0"
    })

@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify(list(recipes.keys()))

@app.route('/recipe/<name>', methods=['GET'])
def get_recipe(name):
    if name in recipes:
        return jsonify(recipes[name])
    else:
        return jsonify({"error": "Recipe not found"}), 404

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "path": file_path})
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/compare', methods=['POST'])
def compare_image():
    data = request.json
    image_path = data.get('image_path')
    instruction = data.get('instruction')
    
    if not image_path or not instruction:
        return jsonify({"error": "Missing image_path or instruction"}), 400
    
    user_image_description, result, feedback = compare_image_with_instruction(image_path, instruction)
    
    return jsonify({
        "user_image_description": user_image_description,
        "result": result,
        "feedback": feedback
    })

if __name__ == '__main__':
    print(f"Starting {app.config['APP_NAME']}...")
    app.run(debug=True)
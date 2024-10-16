import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
from infer import analyze_image
import time 
import requests
import base64

# Set up app and inference client
app = Flask(__name__)
app.config['APP_NAME'] = 'VirtualChef API'
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
client = InferenceClient(api_key=os.getenv("HUGGING_KEY"))

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

def compare_image_with_instruction(user_image_url, recipe, instruction_text):
    """Compare the user's cooking image with the instruction."""
    response = analyze_image(client, user_image_url, "For {}: {}. This image is my result. If completed, only output 'Yes'. If not, BRIEFLY describe what is incorrect.".format(recipe, instruction_text))
    if "Yes" in response:
        return True, "Good job!"
    else:
        return False, response

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

@app.route('/recipes/<name>', methods=['GET'])
def get_recipe(name):
    if name in recipes:
        return jsonify(recipes[name])
    else:
        return jsonify({"error": "Recipe not found"}), 404

@app.route('/compare', methods=['POST'])
def compare_image():
    data = request.json
    recipe = data.get('recipe')
    instruction = data.get('instruction')
    
    if not recipe:
        return jsonify({"error": "Missing recipe"}), 400
    if not instruction:
        return jsonify({"error": "Missing instruction"}), 400
    
    # Local screenshot path
    img_path = "C:\\Users\\rhoss\\Downloads\\VirtualChefScreenshot.png"
    while not os.path.exists(img_path):
        time.sleep(0.1)
    
    # Upload screenshot to Imgur and get public URL

    # Set API endpoint and headers
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": "Client-ID ca006b3450b9e16"}

    # Read image file and encode as base64
    with open(img_path, "rb") as file:
        data = file.read()
        base64_data = base64.b64encode(data)

    # Upload image to Imgur and get URL
    response = requests.post(url, headers=headers, data={"image": base64_data})
    print(response.json())
    url = response.json()["data"]["link"]
    print(url)
    result, feedback = compare_image_with_instruction(url, recipe, instruction)
    os.remove(img_path)
    
    return jsonify({
        "result": result,
        "feedback": feedback
    })

if __name__ == '__main__':
    print(f"Starting {app.config['APP_NAME']}...")
    app.run(debug=True)
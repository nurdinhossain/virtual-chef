import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from huggingface_hub import InferenceClient
from googleapiclient.http import MediaFileUpload
from infer import analyze_image
import pickle
import os.path
import time 

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

SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_to_drive(img_path):
    """Uploads a file to Google Drive using OAuth credentials."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(img_path), 'mimeType': 'image/jpeg'}
    media = MediaFileUpload(img_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id, webViewLink').execute()

    print('File ID: %s' % file.get('id'))
    print('File URL: %s' % file.get('webViewLink'))

    return file.get('webViewLink')

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
    response = analyze_image(client, user_image_url, "I was told to complete this step while cooking {}: {}. This image is my result. If I successfully completed this step, simply output 'Yes'. If I did not, only describe what I did incorrectly.".format(recipe, instruction_text))
    if response == "Yes":
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
    img_path = "C:\\Users\\rhoss\\Downloads\\VirtualChefScreenshot.jpg"
    while not os.path.exists(img_path):
        time.sleep(0.1)
    
    # Upload screenshot to Google Drive and get public URL
    image_url = upload_to_drive(img_path)
    new_url = "https://drive.usercontent.google.com/download?id=" + image_url.split("/d/")[1].split("/")[0]
    print(new_url)
    
    result, feedback = compare_image_with_instruction(new_url, recipe, instruction)
    os.remove(img_path)
    
    return jsonify({
        "result": result,
        "feedback": feedback
    })

if __name__ == '__main__':
    print(f"Starting {app.config['APP_NAME']}...")
    app.run(debug=True)
import os
import sys
import ollama
import cv2
import time

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

# List of cooking instructions for pancakes
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

# List of cooking instructions for quesadillas
quesadilla_instructions = [
    {"instruction": "Heat a non-stick skillet over medium heat."},
    {"instruction": "Place one tortilla in the skillet."},
    {"instruction": "Sprinkle cheese and your choice of fillings (like chicken, beans, or vegetables) on half of the tortilla."},
    {"instruction": "Fold the tortilla in half over the fillings."},
    {"instruction": "Cook until the tortilla is golden brown and the cheese is melted (about 2-3 minutes per side)."},
    {"instruction": "Remove from the skillet and let it cool for a minute."},
    {"instruction": "Cut into wedges and serve with salsa or sour cream."}
]

def capture_image(step_num, recipe_name):
    """Capture an image of the user's cooking for comparison or accept a direct image path."""
    print(f"\n{recipe_name} Step {step_num + 1}: {instructions[step_num]['instruction']}")
    print("Press 'c' to capture an image using your webcam.")
    print("Or enter the path to an existing image file.")
    print("Press 'q' to quit.")

    user_input = input("Your choice (c/path/q): ").strip().lower()

    if user_input == 'c':
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        while True:
            ret, frame = cap.read()
            if not ret:
                raise IOError("Failed to capture image")
            
            cv2.imshow(f"{recipe_name} Cooking Step", frame)
            
            key = cv2.waitKey(1)
            if key == ord('c'):
                img_path = f"user_step_{step_num}.jpg"
                cv2.imwrite(img_path, frame)
                print("Image captured.")
                break
            elif key == ord('q'):
                print("Exiting program.")
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()
        
        cap.release()
        cv2.destroyAllWindows()
    elif user_input == 'q':
        print("Exiting program.")
        sys.exit()
    else:
        img_path = user_input
        if not os.path.exists(img_path):
            print("File does not exist. Please try again.")
            return capture_image(step_num, recipe_name)  
        print(f"Using image: {img_path}")

    return img_path


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

def compare_image_with_instruction(user_image_path, instruction_text):
    """Compare the user's cooking image with the instruction."""
    
    user_image_description = get_image_description(user_image_path)

    res = ollama.chat(
        model="llava:13b",
        messages=[
            {
                "role": "user",
                "content": f"Compare the following image description with the cooking instruction. Does the image show the correct step being performed? Answer with YES if the step is correctly performed, or NO if it's not. Don't judge too harshly and if it includes part of the requirement then mark it correct. Also always assume the best case if there are other possibilities. If the person is also in the process of doing the required step also mark it as correct. Then provide feedback on what's correct and what might be missing or incorrect.\n\nImage Description: {user_image_description}\nInstruction: {instruction_text}"
            }
        ]
    )

    return user_image_description, res["message"]["content"]

def cooking_process(instructions, recipe_name):
    """Main cooking process flow."""
    for step_num, step in enumerate(instructions):
        while True:
            user_image_path = capture_image(step_num, recipe_name)
            
            user_image_description, result = compare_image_with_instruction(user_image_path, step['instruction'])
            
            print(f"\nUser Image Description: {user_image_description}")
            print(f"AI Feedback: {result}")
            
            if result.strip().upper().startswith("YES"):
                print(f"Great job! Step {step_num + 1} complete. Moving to the next step.")
                time.sleep(2)  # Pause to let the user read the feedback
                break
            else:
                print("The AI thinks the step is not completed correctly.")
                user_confirm = input("Do you believe you've completed this step correctly? (y/n): ").lower()
                if user_confirm == 'y':
                    print(f"Understood. Moving to the next step.")
                    time.sleep(2)
                    break
                else:
                    print("Please try again.")
                    print(f"Remember: {step['instruction']}")
                    time.sleep(2)

    print(f"\nCongratulations! You've completed all steps for the {recipe_name}. Enjoy your meal!")

if __name__ == "__main__":
    print("Welcome to the Virtual Chef!")
    print("This program will guide you through making delicious recipes.")
    print("Make sure you have all ingredients ready before starting.")
    
    print("\n1. Omelette")
    print("2. Pancakes")
    print("3. Quesadillas")
    choice = input("Which recipe would you like to follow? (1/2/3): ").strip()
    
    if choice == '1':
        instructions = omelette_instructions
        recipe_name = "Omelette"
    elif choice == '2':
        instructions = pancake_instructions
        recipe_name = "Pancakes"
    elif choice == '3':
        instructions = quesadilla_instructions
        recipe_name = "Quesadillas"
    else:
        print("Invalid choice. Exiting program.")
        sys.exit()
    
    input("Press Enter when you're ready to begin...")
    cooking_process(instructions, recipe_name)
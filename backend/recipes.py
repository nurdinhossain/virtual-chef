import os
import sys
import ollama
import cv2
import time

# List of cooking instructions for a simple omelette
instructions = [
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

def capture_image(step_num):
    """Capture an image of the user's cooking for comparison or accept a direct image path."""
    print(f"\nStep {step_num + 1}: {instructions[step_num]['instruction']}")
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
            
            cv2.imshow("Cooking Step", frame)
            
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
        # Assume the input is a file path
        img_path = user_input
        if not os.path.exists(img_path):
            print("File does not exist. Please try again.")
            return capture_image(step_num)  # Recursive call to retry
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
                "content": f"Compare the following image description with the cooking instruction. Does the image show the correct step being performed? Answer with YES if the step is correctly performed, 
                or NO if it's not. Don't judge too harshly and if it includes part of the requirement then mark it correct. Also always assume the best case if there are other possibilities. 
                If the person is also in the process of doing the required step also mark it as correct.
                Then provide feedback on what's correct and what might be missing or incorrect.\n\nImage Description: {user_image_description}\nInstruction: {instruction_text}"
            }
        ]
    )

    return user_image_description, res["message"]["content"]

def cooking_process():
    """Main cooking process flow."""
    for step_num, step in enumerate(instructions):
        while True:
            user_image_path = capture_image(step_num)
            
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

    print("\nCongratulations! You've completed all steps. Enjoy your omelette!")


if __name__ == "__main__":
    print("Welcome to the Virtual Chef!")
    print("This program will guide you through making a delicious omelette.")
    print("Make sure you have all ingredients ready before starting.")
    input("Press Enter when you're ready to begin...")
    cooking_process()

import os
import sys
import ollama
import cv2

# List of cooking instructions
instructions = [
    {"instruction": "Chop the onions."},
    # Add more instructions as needed
]

def capture_image(step_num):
    """Capture an image of the user's cooking for comparison."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    print(f"Step {step_num + 1}: {instructions[step_num]['instruction']}")
    print("Press 'c' to capture an image or 'q' to quit.")
    
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
    return img_path

def get_image_description(image_path):
    """Get a description of the image from the API."""
    res = ollama.chat(
        model="llava:13b",
        messages=[
            {
                "role": "user",
                "content": f"Describe the contents of the image at {image_path}.",
                "images": [image_path]
            }
        ]
    )
    return res["message"]["content"]

def compare_image_with_instruction(user_image_path, instruction_text):
    """Compare the user's cooking image with the instruction."""
    
    # Get description for the user image
    user_image_description = get_image_description("/Users/aali11/Documents/virtual-chef/backend/BHG-chopping-an-onion-hero-01-50781-ae9396e13bbd4ab6b779fcb425049957.jpg") #Replace with user_image_path in final implementation 

    # Compare image description with instruction
    res = ollama.chat(
        model="llava:13b",
        messages=[
            {
                "role": "user",
                "content": f"Does the following image description match the instruction?\n\nImage Description: {user_image_description}\nInstruction: {instruction_text}"
            }
        ]
    )

    return user_image_description, res["message"]["content"]

def cooking_process():
    """Main cooking process flow."""
    for step_num, step in enumerate(instructions):
        print(f"Step {step_num + 1}: {step['instruction']}")
        
        # Capture user image for this step
        user_image_path = capture_image(step_num)
        
        # Compare with instruction
        user_image_description, result = compare_image_with_instruction(user_image_path, step['instruction'])
        
        print(f"\nInstruction: {step['instruction']}")
        print(f"User Image Description: {user_image_description}")
        print(f"Comparison result: {result}")
        
        if "match" in result.lower():
            print(f"Step {step_num + 1} complete! Moving to the next step.")
        else:
            print("The image does not match the instruction. Please retry the step.")
            step_num -= 1  

if __name__ == "__main__":
    cooking_process()

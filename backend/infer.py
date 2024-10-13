import os
from huggingface_hub import InferenceClient
import base64

client = InferenceClient(api_key=os.getenv("HUGGING_KEY"))

image_url = "https://thedeliciousspoon.com/french-toast-pancakes/pancake-process-6/"

def analyze_image(client, img_url, prompt):
    result = ""
    for message in client.chat_completion(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": img_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        max_tokens=500,
        stream=True,
    ):
        result += message.choices[0].delta.content

    return result
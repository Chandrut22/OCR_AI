import os
import google.generativeai as genai
import mimetypes
from dotenv import load_dotenv


load_dotenv()

def generate():
    
    api_key = os.getenv("GEMINI_API_KEY") 

    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set in .env file.")
        return  # Exit if the API key is missing

    genai.configure(api_key=api_key)

    
    file_path = "New folder\\WhatsApp Image 2025-03-07 at 15.51.53_b859b5ce.jpg"
    mime_type = mimetypes.guess_type(file_path)[0]

    if not mime_type:
        mime_type = "application/octet-stream"  

    with open(file_path, "rb") as f:
        file_data = f.read()

    image_part = {"mime_type": mime_type, "data": file_data}


    model = "gemini-2.0-flash"  
    parts = [image_part, "what text is in the image?"]


    generation_config = genai.GenerationConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
    )

    model = genai.GenerativeModel(model_name=model)  # Initialize the model

    try:
        response = model.generate_content(
            parts, generation_config=generation_config, stream=True
        )

        for chunk in response:
            print(chunk.text, end="")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")



generate()
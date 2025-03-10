import os
import mimetypes
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set in .env file.")

genai.configure(api_key=api_key)

def extract_text_from_image(file):
    """Process the image with Gemini API and return extracted text."""
    mime_type = mimetypes.guess_type(file.filename)[0]
    if not mime_type:
        mime_type = "application/octet-stream"

    image_part = {"mime_type": mime_type, "data": file.read()}

    model = "gemini-2.0-flash"
    parts = [image_part, "What text is in the image?"]

    generation_config = genai.GenerationConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
    )

    model = genai.GenerativeModel(model_name=model)

    try:
        response = model.generate_content(
            parts, generation_config=generation_config, stream=True
        )

        extracted_text = "".join(chunk.text for chunk in response)
        return extracted_text

    except Exception as e:
        return str(e)

@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads and return extracted text."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        extracted_text = extract_text_from_image(file)
        return jsonify({"result": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

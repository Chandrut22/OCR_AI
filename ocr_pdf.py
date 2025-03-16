from mistralai import Mistral
import os

api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

uploaded_pdf = client.files.upload(
    file={
        "file_name": "sample",
        "content": open(r"C:\Users\thamb\Downloads\Machine Learning by TutorialsPoint.pdf", "rb"),
    },
    purpose="ocr"
)  

print(uploaded_pdf)

signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)


ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url,
    },
    include_image_base64=True
)

# Assuming `ocr_response` is an object and not a dictionary

# Extract text from all pages
# document_text = "\n\n".join(page.markdown for page in pages)  # Use dot notation

# Print extracted text
# print(document_text)

# print(pages)

import json

# Function to convert objects to dictionaries
def serialize(obj):
    """Recursively convert objects to dictionaries for JSON serialization."""
    if isinstance(obj, list):
        return [serialize(item) for item in obj]  # Convert lists recursively
    elif hasattr(obj, "__dict__"):  
        return {key: serialize(value) for key, value in obj.__dict__.items()}  # Convert objects to dicts
    else:
        return obj  # Return as-is for primitives

# Extract and serialize pages
pages = ocr_response.pages
pages_data = serialize(pages)  # Convert OCR response into JSON-serializable format

# Save as JSON file
with open("ocr_output.json", "w", encoding="utf-8") as json_file:
    json.dump(pages_data, json_file, indent=4, ensure_ascii=False)

print("OCR response saved as ocr_output.json")



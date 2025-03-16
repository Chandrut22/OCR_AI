import base64
import os
import mimetypes
import time
from mistralai import Mistral
from dotenv import load_dotenv

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_image(image_path, client):
    """Process an image file with OCR."""
    base64_image = encode_image(image_path)
    if base64_image:
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            }
        )
        return response.get("text", "No text found")  # Extract OCR text from response
    return None

def process_pdf(pdf_path, client):
    """Upload and process a PDF file with OCR."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            upload_response = client.files.upload(
                file={
                    "file_name": os.path.basename(pdf_path),
                    "content": pdf_file.read(),
                },
                purpose="ocr"
            )

        # Extract text after upload
        file_id = upload_response.id  # Ensure this matches your API's response structure
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "file_id", "file_id": file_id}
        )

        return ocr_response.text if hasattr(ocr_response, "text") else None
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
    except Exception as e:
        print(f"Error: {e}")
    return None


def save_output(text, filename, file_format):
    """Save the OCR result in the desired format."""
    if isinstance(text, tuple):  # Ensure it's a string
        text = "\n".join(text)

    if file_format == "txt":
        with open(filename + ".txt", "w", encoding="utf-8") as file:
            file.write(text)
    elif file_format == "pdf":
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(filename + ".pdf")
    elif file_format == "docx":
        from docx import Document
        doc = Document()
        doc.add_paragraph(text)
        doc.save(filename + ".docx")
    else:
        print("Invalid format selected.")
        return
    
    print(f"OCR results saved as {filename}.{file_format}")

# Load environment variables
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    print("Error: MISTRAL_API_KEY environment variable not set.")
    exit()

client = Mistral(api_key=api_key)

# User input for file selection
file_path = input("Enter the file path (image or PDF): ")
file_type, _ = mimetypes.guess_type(file_path)

if file_type:
    if file_type.startswith("image"):
        ocr_text = process_image(file_path, client)
    elif file_type == "application/pdf":
        ocr_text = process_pdf(file_path, client)
    else:
        print("Unsupported file type.")
        exit()
else:
    print("Could not determine file type.")
    exit()

if ocr_text:
    print("OCR Result:", ocr_text[:500])  # Print only first 500 chars for preview
    save_choice = "docx"  # Change to "pdf" or "txt" if needed
    output_filename = "ocr_output"
    save_output(ocr_text, output_filename, save_choice)
else:
    print("No text extracted from the file.")

import fitz  # PyMuPDF

def extract_embedded_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    
    for page_number, page in enumerate(doc):
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{output_folder}/page_{page_number + 1}_img_{img_index + 1}.{image_ext}"

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            print(f"Saved: {image_path}")

# Example usage
extract_embedded_images(r"C:\Users\thamb\Downloads\Machine Learning by TutorialsPoint.pdf", "output_images")

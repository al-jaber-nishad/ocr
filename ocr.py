import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# Set the TESSDATA_PREFIX environment variable
# os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/"  # Update this path accordingly

def extract_text_with_ocr(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Variable to hold all extracted text
    extracted_text = ""
    
    # Loop through each page
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)
        # Extract text using PyMuPDF
        text = page.get_text("text")
        # Append the text to our variable
        extracted_text += text + "\n"
        
        # If direct text extraction is not good enough, do OCR
        if "some_condition_to_check_bad_extraction":  # Replace this with actual condition or logic to check quality
            # Extract the page as an image
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            # Use pytesseract to do OCR on the image
            ocr_text = pytesseract.image_to_string(img, lang='ben+eng')  # Use both Bangla and English
            # Append the OCR text to our variable
            extracted_text += ocr_text + "\n"
    
    return extracted_text

def save_text_to_file(text, output_path):
    # Save the text to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

# Specify the path to your PDF file
pdf_path = "file.pdf"

# Extract text from the PDF
extracted_text = extract_text_with_ocr(pdf_path)

# Specify the output file path
output_text_file = "extracted_text.txt"

# Save the extracted text to a file
save_text_to_file(extracted_text, output_text_file)

print(f"Extracted text has been saved to {output_text_file}")

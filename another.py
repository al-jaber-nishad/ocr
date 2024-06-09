import pdfplumber
import re
import pytesseract
from PIL import Image
import json


def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='ben+eng')  # Specify Bengali and English languages
    return text


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_image_from_pdf(pdf_path, page_num, image_type):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        if not page.images:
            print(f"No images found on page {page_num}")
            return None
        
        if image_type == 'Person image':
            # Assuming the person image is the first image on the page
            if len(page.images) > 0:
                image = page.images[0]
            else:
                print(f"No 'Person image' found on page {page_num}")
                return None
        elif image_type == 'Person signature':
            # Assuming the signature is the second image on the page
            if len(page.images) > 1:
                image = page.images[1]
            else:
                print(f"No 'Person signature' found on page {page_num}")
                return None
        
        image_bbox = (image['x0'], image['top'], image['x1'], image['bottom'])
        image_cropped = page.within_bbox(image_bbox)
        pil_image = image_cropped.to_image().original

        image_path = f"{image_type.replace(' ', '_')}.png"
        pil_image.save(image_path)
        return image_path


def extract_key_value_pairs(text):
    data = {}
    key_value_patterns = {
        'National ID': r'National ID (\d+)',
        'Pin': r'Pin (\d+)',
        'Name(Bangla)': r'Name\(Bangla\) (.+)',
        'Name(English)': r'Name\(English\) (.+)',
        'Date of Birth': r'Date of Birth (\d{4}-\d{2}-\d{2})',
        'Birth Place': r'Birth Place (.+)',
        'Father Name': r'Father Name (.+)',
        'Mother Name': r'Mother Name (.+)',
        # 'Blood Group': r'Blood Group (.+)',
        'District': r'District (.+)',
        # 'City Corporation Or Municipality': r'City Corporation Or Municipality (.+)',
        'Upozila': r'Upozila (.+)',
        # 'Additional Mouza/Moholla': r'Additional Mouza/Moholla (.+)',
        # 'Additional Village/Road': r'Additional Village/Road (.+)',
        # 'Village/Road': r'Village/Road (.+)',
        'Home/Holding No': r'Home/HoldingNo (.+)',
        'Postal Code': r'Postal Code (\d+)',
        'Post Office': r'Post Office (.+)'
    }

    for key, pattern in key_value_patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip()

    return data



def extract_words(text):
    # Extended regex pattern to match all Bengali characters, including joint characters
    bengali_pattern = re.compile(r'[\u0980-\u09FF\u200C-\u200D]+')
    # Regex pattern to match English words
    english_pattern = re.compile(r'[a-zA-Z]+')

    bengali_words = bengali_pattern.findall(text)
    english_words = english_pattern.findall(text)

    return bengali_words, english_words


def main(pdf_path):
    
    # Extract images (assuming images are on the first page)
    person_image_path = extract_image_from_pdf(pdf_path, 4, 'Person image')
    person_signature_path = extract_image_from_pdf(pdf_path, 4, 'Person signature')

    # Extract key-value pairs from the text
    text = extract_text_from_pdf(pdf_path)

    bengali_words, english_words = extract_words(text)
    print(bengali_words)

    data = extract_key_value_pairs(text)
    data['Person image'] = person_image_path
    data['Person signature'] = person_signature_path

    # Save the extracted data to a JSON file
    with open('extracted_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Path to the PDF file
pdf_path = 'data.pdf'

# Run the main function
main(pdf_path)

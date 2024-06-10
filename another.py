import pdfplumber
import re
import pytesseract
from PIL import Image
import json
import cv2
import numpy as np
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, dpi=300):
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi)
    image_paths = []
    for i, img in enumerate(images):
        image_path = f'page_{i}.png'
        img.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths

def preprocess_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to binarize the image
    binary_image = cv2.adaptiveThreshold(gray, 255, 
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get bounding box of largest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # Crop the image to the bounding box
        cropped_image = image[y:y+h, x:x+w]
    else:
        cropped_image = image

    # Resize the cropped image to simulate a higher DPI
    height, width = cropped_image.shape[:2]
    new_height = int(height * 2)  # Increase height by 2 times
    new_width = int(width * 2)  # Increase width by 2 times
    resized_image = cv2.resize(cropped_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale and binarize again
    gray_resized = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    binary_resized = cv2.adaptiveThreshold(gray_resized, 255, 
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 11, 2)
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    binary_resized = cv2.dilate(binary_resized, kernel, iterations=1)
    binary_resized = cv2.erode(binary_resized, kernel, iterations=1)

    # Save the processed image
    processed_image_path = image_path.replace('.png', '_processed.png')
    cv2.imwrite(processed_image_path, binary_resized)
    return processed_image_path

def extract_text_from_image(image_path):
    # Preprocess the image
    processed_image_path = preprocess_image(image_path)
    # Open the processed image file
    img = Image.open(processed_image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='ben+eng')  # Specify Bengali and English languages
    return text

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

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
    # Extract images from the PDF and process them
    image_paths = pdf_to_images(pdf_path)

    extracted_texts = []
    for image_path in image_paths:
        text = extract_text_from_image(image_path)
        extracted_texts.append(text)

    # Extract text directly from the PDF
    text_from_pdf = extract_text_from_pdf(pdf_path)

    # Combine texts
    combined_text = text_from_pdf + "\n" + "\n".join(extracted_texts)

    # Extract key-value pairs from the combined text
    data = extract_key_value_pairs(combined_text)
    print("data", data)
    bengali_words, english_words = extract_words(combined_text)

    # Save the extracted data to a JSON file
    with open('extracted_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Path to the PDF file
pdf_path = 'data.pdf'

# Run the main function
main(pdf_path)

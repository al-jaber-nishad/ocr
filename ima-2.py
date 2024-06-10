from PIL import Image
import pytesseract
import re
from pdf2image import convert_from_path
import os

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='ben+eng')  # Specify Bengali and English languages
    return text

# def print_unicode_characters(text):
#     for char in text:
#         print(f"Character: {char}, Unicode: {ord(char)}")

def join_bengali_characters(text):
    # Join characters correctly, considering Bengali joint characters
    joined_text = ''
    for char in text:
        if char in '\u0980-\u09FF\u200C-\u200D':  # Bengali characters and zero-width joiners
            joined_text += char
        else:
            joined_text += ' ' + char + ' '
    return re.sub(r'\s+', ' ', joined_text).strip()

def extract_words(text):
    # Extended regex pattern to match all Bengali characters, including joint characters
    bengali_pattern = re.compile(r'[\u0980-\u09FF\u200C-\u200D]+')
    # Regex pattern to match English words
    english_pattern = re.compile(r'[a-zA-Z]+')

    bengali_words = bengali_pattern.findall(text)
    english_words = english_pattern.findall(text)

    return bengali_words, english_words

# Path to the image file
# image_path = 'output_images/page_1.png'


image_path = 'image.png'

def convert_pdf_to_images(pdf_path, output_folder, dpi=120):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert PDF pages to images with specified DPI
    images = convert_from_path(pdf_path, dpi=dpi)
    
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

def crop_image_to_content(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Convert image to grayscale
    gray_image = image.convert('L')
    
    # Create a binary image (black and white)
    binary_image = gray_image.point(lambda x: 0 if x == 255 else 255, '1')
    
    # Find the bounding box of the non-zero regions in the binary image
    bbox = binary_image.getbbox()
    
    if bbox:
        # Crop the image to the bounding box
        cropped_image = image.crop(bbox)
        # Save the cropped image, replacing the original image
        cropped_image.save(image_path)
    else:
        print("No content found to crop.")

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
        'Spouse Name': r'Spouse Name (.+)',
        'Blood Group': r'Blood Group (.+)',
        'District': r'District (.+)',
        'City Corporation Or Municipality': r'City Corporation Or Municipality (.+)',
        'Upozila': r'Upozila (.+)',
        'Additional Mouza/Moholla': r'Additional Mouza/Moholla (.+)',
        'Additional Village/Road': r'Additional Village/Road (.+)',
        'Village/Road': r'Village/Road (.+)',
        'Home/Holding No': r'Home/HoldingNo (.+)',
        'Postal Code': r'Postal Code (\d+)',
        'Post Office': r'Post Office (.+)'
    }

    for key, pattern in key_value_patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip()

    return data


# Path to the PDF file
pdf_path = 'file.pdf'
# Folder to save the images
output_folder = 'output_img'

# Convert PDF to images
image_paths = convert_pdf_to_images(pdf_path, output_folder)

total_text = []
bengali_words = []
english_words = []
# Print the paths of the saved images
for image_path in image_paths:
    crop_image_to_content(image_path)
    
    image_text = extract_text_from_image(image_path)
    total_text.append(image_text)

    print(image_path)
    print(image_text)

    bengali, english = extract_words(image_text)
    bengali_words.append(bengali)
    english_words.append(english)

total_text = "\n".join(total_text)
data = extract_key_value_pairs(total_text)
print("data", data)





# image_text = ""
# Extract text from the image

# Print each character's Unicode
# print_unicode_characters(image_text)

# Join separated Bengali characters correctly
# corrected_text = join_bengali_characters(image_text)

# Extract Bengali and English words

ben_str = ""
for word in bengali_words:
    for item in word:
        ben_str += " "+item


def save_text_to_file(text, output_path):
    # Save the text to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)



# Specify the output file path
output_text_file = "extracted_text.txt"


# Save the extracted text to a file
save_text_to_file(ben_str, output_text_file)

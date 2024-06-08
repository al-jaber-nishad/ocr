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

def convert_pdf_to_images(pdf_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)
    
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

# Path to the PDF file
pdf_path = 'file.pdf'
# Folder to save the images
output_folder = 'output_img'

# Convert PDF to images
image_paths = convert_pdf_to_images(pdf_path, output_folder)

# image_text = []
bengali_words = []
english_words = []
# Print the paths of the saved images
for image_path in image_paths:
    print(image_path)

    image_text = extract_text_from_image(image_path)

    bengali, english = extract_words(image_text)
    bengali_words.append(bengali)
    english_words.append(english)








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


# Print the results
print("Bengali Words:", bengali_words)
print("English Words:", english_words)

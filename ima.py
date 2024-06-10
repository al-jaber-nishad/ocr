from PIL import Image
import pytesseract
import re

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
# image_path = 'image.png'
image_path = 'page_0.png'

# Extract text from the image
image_text = extract_text_from_image(image_path)

# Print each character's Unicode
# print_unicode_characters(image_text)

# Join separated Bengali characters correctly
# corrected_text = join_bengali_characters(image_text)

# Extract Bengali and English words
bengali_words, english_words = extract_words(image_text)

ben_str = ""
for item in bengali_words:
    ben_str += " "+item

print("bengali_words", ben_str)

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

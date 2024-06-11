from PIL import Image
import pytesseract
import re
from pdf2image import convert_from_path
import os
import pdfplumber


key_list = [
    "Upozila",
    "Union/Ward",
    "Post Office"
]

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='ben+eng')  # Specify Bengali and English languages
    return text

def extract_image_from_pdf(pdf_path, page_num, image_type):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        if image_type == 'Person image':
            # Assuming the person image is the first image on the page
            image = page.images[0]
        elif image_type == 'Person signature':
            # Assuming the signature is the second image on the page
            image = page.images[1]
        
        image_bbox = (image['x0'], image['top'], image['x1'], image['bottom'])
        image_cropped = page.within_bbox(image_bbox)
        pil_image = image_cropped.to_image().original

        image_path = f"{image_type.replace(' ', '_')}.png"
        pil_image.save(image_path)
        return image_path
    

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

# def extract_key_value_pairs(text):
#     data = {}
#     key_value_patterns = {
#         'National ID': r'National ID:?\s*([\d-]+)',
#         'Pin': r'Pin:?\s*([\d-]+)',
#         'Name(Bangla)': r'Name\(Bangla\):?\s*(.+)',
#         'Name(English)': r'Name\(English\):?\s*(.+)',
#         'Date of Birth': r'Date of Birth:?\s*([\d-]+)',
#         'Birth Place': r'Birth Place:?\s*(.+)',
#         'Father Name': r'Father Name:?\s*(.+)',
#         'Mother Name': r'Mother Name:?\s*(.+)',
#         'Spouse Name': r'Spouse Name:?\s*(.+)',
#         'Blood Group': r'Blood Group:?\s*(.+)',
#         'Education': r'Education:?\s*(.+)',
#         'District': r'District:?\s*(.+)',
#         'City Corporation Or Municipality': r'City Corporation Or Municipality:?\s*(.+)',
#         'Upozila': r'Upozila:?\s*(.+)',
#         'Additional Mouza/Moholla': r'Additional Mouza/Moholla:?\s*(.+)',
#         'Additional Village/Road': r'Additional Village/Road:?\s*(.+)',
#         'Village/Road': r'Village/Road:?\s*(.+)',
#         'Home/Holding No': r'Home/HoldingNo:?\s*(.+)',
#         'Postal Code': r'Postal Code:?\s*([\d-]+)',
#         'Post Office': r'Post Office:?\s*(.+)'
#     }

#     for key, pattern in key_value_patterns.items():
#         match = re.search(pattern, text)
#         if match:
#             data[key] = match.group(1).strip()

#     return data


def extract_key_value_pairs(text):
    data = {}
    key_value_patterns = {
        'National ID': r'National ID:?\s*([\d-]+)',
        'Pin': r'Pin:?\s*([\d-]+)',
        'Name(Bangla)': r'Name\(Bangla\):?\s*(.+)',
        'Name(English)': r'Name\(English\):?\s*(.+)',
        'Date of Birth': r'Date of Birth:?\s*([\d-]+)',
        'Birth Place': r'Birth Place:?\s*(.+)',
        'Father Name': r'Father Name:?\s*(.+)',
        'Mother Name': r'Mother Name:?\s*(.+)',
        'Spouse Name': r'Spouse Name:?\s*(.+)',
        'Blood Group': r'Blood Group:?\s*(.+)',
        'Education': r'Education:?\s*(.+)',
        'District': r'District:?\s*(.+)',
        'City Corporation Or Municipality': r'City Corporation Or Municipality:?\s*(.+)',
        'Upozila': r'Upozila:?\s*(.+)',
        'Union/Ward': r'Union/Ward:?\s*(.+)',
        'Additional Mouza/Moholla': r'Additional Mouza/Moholla:?\s*(.+)',
        'Additional Village/Road': r'Additional Village/Road:?\s*(.+)',
        'Village/Road': r'Village/Road:?\s*(.+)',
        'Home/Holding No': r'Home/HoldingNo:?\s*(.+)',
        'Postal Code': r'Postal Code:?\s*([\d-]+)',
        'Post Office': r'Post Office:?\s*(.+)'
    }

    key_list = [
        "Upozila",
        "Union/Ward",
        "Post Office"
    ]

    lines = text.split('\n')
    for line in lines:
        for key, pattern in key_value_patterns.items():
            match = re.match(pattern, line.strip())
            if match:
                data[key] = match.group(1).strip()

    # Handle overlapping values for specific keys
    for key in key_list:
        if key in data:
            value = data[key]
            # Split value by space and reassign parts to correct keys if needed
            parts = value.split()
            for part in parts:
                if re.match(r'^\d{4,}$', part):  # Check for a postal code
                    data['Postal Code'] = part
                    data[key] = value.replace(part, '').strip()
                elif part.lower() in ['postal', 'code']:
                    data['Postal Code'] = parts[-1]
                    data[key] = ' '.join(parts[:-2]).strip()

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

    # print(image_path)
    # print(image_text)

    bengali, english = extract_words(image_text)
    bengali_words.append(bengali)
    english_words.append(english)

total_text = "\n".join(total_text)

print("total_text", total_text)

data = extract_key_value_pairs(total_text)

# # Extract images (assuming images are on the first page)
# person_image_path = extract_image_from_pdf(pdf_path, 0, 'Person image')
# person_signature_path = extract_image_from_pdf(pdf_path, 0, 'Person signature')

# # Extract key-value pairs from the text
# data['Person image'] = person_image_path
# data['Person signature'] = person_signature_path


# print("data", data)



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

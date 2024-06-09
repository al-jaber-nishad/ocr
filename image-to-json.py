import cv2
import numpy as np
from PIL import Image
import pytesseract
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

def enhance_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to binarize the image
    binary_image = cv2.adaptiveThreshold(blurred, 255, 
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 11, 2)
    return binary_image

def crop_image_to_content_cv(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    binary_image = enhance_image(image)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get bounding box of largest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # Expand the bounding box a bit
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)

        # Crop the image to the bounding box
        cropped_image = image[y:y+h, x:x+w]
        # Save the cropped image, replacing the original image
        cv2.imwrite(image_path, cropped_image)
    else:
        print("No content found to crop.")
        cropped_image = image  # If no contours are found, use the original image

    return cropped_image

def extract_text_from_image(image):
    # Convert the OpenCV image to PIL format
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img_pil, lang='ben+eng')
    return text

def main(pdf_path):
    # Convert PDF to images
    image_paths = pdf_to_images(pdf_path)
    
    extracted_texts = {}

    for image_path in image_paths:
        cropped_image = crop_image_to_content_cv(image_path)
        text = extract_text_from_image(cropped_image)
        print(f"Text from {image_path}:")
        print(text)
        extracted_texts[image_path] = text

# Path to the PDF file
pdf_path = 'file.pdf'

# Run the main function
main(pdf_path)

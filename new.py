import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_words(text):
    # Regex pattern to match Bengali characters
    bengali_pattern = re.compile(r'[\u0980-\u09FF\u200C-\u200D]+')
    # Regex pattern to match English words
    english_pattern = re.compile(r'[a-zA-Z]+')

    bengali_words = bengali_pattern.findall(text)
    english_words = english_pattern.findall(text)

    return bengali_words, english_words


def save_text_to_file(text, output_path):
    # Save the text to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)


# Path to the PDF file
pdf_path = 'file.pdf'

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Extract Bengali and English words
bengali_words, english_words = extract_words(pdf_text)

ben_str = ""
for item in bengali_words:
    ben_str += " "+item

# Specify the output file path
output_text_file = "extracted_bangla_text.txt"

# Save the extracted text to a file
save_text_to_file(ben_str, output_text_file)

# Print the results
print("Bengali Words:", bengali_words)
# print("English Words:", english_words)


def encode(list):
    b = [chr(number) for number in list]
    return print(b)

# Vowels (স্বরবর্ণ)
Vowels = [2437, 2438, 2439, 2440, 2441, 2442, 2443, 2447, 2448, 2451, 2452]

# Numbers (সংখ্যা)
Numbers = [2534, 2535, 2536, 2537, 2538, 2539, 2540, 2541, 2542, 2543]

# Consonants (ব্যঞ্জনবর্ণ)
Consonants = [2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2472, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2482, 2486, 2487, 2488, 2489, 2524, 2525, 2527, 2510, 2433, 2434, 2435]

# Vowel Diacritics (কার)
Vowel_Diacritics = [2494, 2495, 2496, 2497, 2498, 2499, 2503, 2504, 2507, 2508]

# Vowels + Numbers + Consonants + Vowel Diacritics
All = [2437, 2438, 2439, 2440, 2441, 2442, 2443, 2447, 2448, 2451, 2452, 2534, 2535, 2536, 2537, 2538, 2539, 2540, 2541, 2542, 2543, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2472, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2482, 2486, 2487, 2488, 2489, 2524, 2525, 2527, 2510, 2433, 2434, 2435, 2494, 2495, 2496, 2497, 2498, 2499, 2503, 2504, 2507, 2508]

encode(Vowels)
encode(Numbers)
encode(Consonants)
encode(Vowel_Diacritics)
encode(All)
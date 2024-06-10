# import re

# # Example mapping of CID values to Unicode characters (this is just a small sample)
# cid_to_unicode = {
#     381: 'ড',
#     207: 'মা',
#     387: 'হ'
#     # Add more mappings as needed
# }

# def replace_cid_with_unicode(text, cid_mapping):
#     # Pattern to find all occurrences of (cid:xxx) where xxx is a number
#     cid_pattern = re.compile(r'\(cid:(\d+)\)')
    
#     def cid_replacer(match):
#         cid_value = int(match.group(1))
#         return cid_mapping.get(cid_value, match.group(0))  # Replace or keep original if not found

#     return cid_pattern.sub(cid_replacer, text)

# # Example text with CID values
# text = 'ব(cid:381)ড়া (cid:207)মাঃ (cid:387)ল ইসলাম'

# # Replace CID values with Unicode characters
# decoded_text = replace_cid_with_unicode(text, cid_to_unicode)

# print("Original Text:", text)
# print("Decoded Text:", decoded_text)


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

def extract_cid_mapping(pdf_path):
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        # Process each page contained in the document.
        for page in PDFPage.create_pages(document):
            # Access the fonts and encoding from the page resources
            if 'Resources' in page.attrs:
                resources = page.attrs['Resources']
                if 'Font' in resources:
                    fonts = resources['Font']
                    for font in fonts.values():
                        print("fonts", font)
                        # Extract CID to Unicode mapping from font object
                        if hasattr(font, 'decode'):
                            cmap = font.decode().cmap
                            for cid, unicode_char in cmap.items():
                                print(f'CID {cid} -> {unicode_char}')

# Path to your PDF file
pdf_path = 'file.pdf'

# Extract CID to Unicode mapping
extract_cid_mapping(pdf_path)

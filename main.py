import os
import pytesseract
import cv2
# Add the pdf2image library to transform all the pages of the PDF into images

image_path = r"" # Insert the path to the image you want to extract text from

path_tesseract = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = os.path.join(path_tesseract, "tesseract.exe")

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

text = extract_text_from_image(image_path)
print(text)

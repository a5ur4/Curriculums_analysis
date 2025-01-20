import os
import pytesseract
import cv2
from pdf2image import convert_from_path

folder_path = r"C:\Users\pedro\Downloads\curriculums"
path_tesseract = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = os.path.join(path_tesseract, "tesseract.exe")
poppler_path = r"C:\poppler\Library\bin"

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        
        images = convert_from_path(file_path, poppler_path=poppler_path)
        
        for i, image in enumerate(images):
            image_path = f"{filename}_page_{i}.png"
            image.save(image_path, "PNG")
            
            text = pytesseract.image_to_string(cv2.imread(image_path))
            print(text)
            os.remove(image_path)
            
        print(f"Analisando: {filename}")

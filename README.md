# Curriculum Analyzer

This project is a Python script that analyzes PDF files containing curriculums (CVs) to extract contact information, work experience, and keywords related to specific technologies. The results are saved in an Excel file.

## Requirements

- Python 3.x
- pytesseract
- opencv-python
- openpyxl
- pdf2image

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

    ```sh
    pip install pytesseract opencv-python openpyxl pdf2image
    ```

3. Install Tesseract OCR and Poppler:
    - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
    - [Poppler](http://blog.alivate.com.au/poppler-windows/)

## Usage

1. Place the PDF files containing the curriculums in a folder.
2. Update the [folder_path](http://_vscodecontentref_/1), [path_tesseract](http://_vscodecontentref_/2), [poppler_path](http://_vscodecontentref_/3), [save_path](http://_vscodecontentref_/4), and [txt_save_path](http://_vscodecontentref_/5) variables in the script to point to the appropriate directories.
3. Run the script:

    ```sh
    python main.py
    ```

4. The script will analyze the PDF files, convert them to images, extract text, and save the results in an Excel file.

## Script Details

- The script searches for the following keywords in the curriculums: `Java`, `Spring`, `Python`, `Django`, `JavaScript`, `React`, `Node`, `SQL`, `NoSQL`, `MongoDB`, `PostgreSQL`, `MySQL`, `HTML`, `CSS`, `Bootstrap`.
- It extracts contact information (phone numbers and email addresses) and work experience (time periods and roles).
- The script approves a curriculum if it contains more than 5 of the specified keywords.

## Functions

- [convert_to_image(file_path, poppler_path, save_path)](http://_vscodecontentref_/6): Converts PDF files to images.
- [extract_text(image_path)](http://_vscodecontentref_/7): Extracts text from images using Tesseract OCR.
- [extract_name_from_text(text)](http://_vscodecontentref_/8): Extracts names from the given text.

## Output

The results are saved in an Excel file with the following columns:
- `Arquivo`: The name of the PDF file.
- `Telefones`: Extracted phone numbers.
- `E-mails`: Extracted email addresses.
- `Palavras-chave encontradas`: Keywords found in the curriculum.
- `Quantidade de palavras-chave`: Number of keywords found.
- `Experiências`: Extracted work experience details.
- `Aprovado`: Whether the curriculum is approved or not.

## License

This project is licensed under the MIT License.
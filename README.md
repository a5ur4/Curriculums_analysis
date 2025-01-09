# Curriculum Analyzer

This project is a Python script that analyzes PDF files containing curriculums (CVs) to extract contact information, work experience, and keywords related to specific technologies. The results are saved in an Excel file.

## Requirements

- Python 3.x
- pandas
- pdfplumber

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

    ```sh
    pip install pandas pdfplumber
    ```

## Usage

1. Place the PDF files containing the curriculums in a folder.
2. Update the [folder_path](http://_vscodecontentref_/1) variable in the script to point to the folder containing the PDF files.
3. Run the script:

    ```sh
    python script.py
    ```

4. The script will analyze the PDF files and save the results in an Excel file named `curriculums_analysis.xlsx`.

## Script Details

- The script searches for the following keywords in the curriculums: `Java`, `Spring`, `Python`, `Django`, `JavaScript`, `React`, `Node`, `SQL`, `NoSQL`, `MongoDB`, `PostgreSQL`, `MySQL`, `HTML`, `CSS`, `Bootstrap`.
- It extracts contact information (phone numbers and email addresses) and work experience (time periods and roles).
- The script approves a curriculum if it contains more than 5 of the specified keywords.

## Functions

- [extract_contact(text)](http://_vscodecontentref_/2): Extracts phone numbers and email addresses from the given text.
- [extract_experience(text)](http://_vscodecontentref_/3): Extracts work experience details from the given text.
- [approved(found_keywords)](http://_vscodecontentref_/4): Determines if a curriculum is approved based on the number of keywords found.

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
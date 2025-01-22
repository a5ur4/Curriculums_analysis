import os
import pytesseract
import cv2
import openpyxl
import re
import logging
from pdf2image import convert_from_path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

folder_path = r"C:\Users\pedro\Downloads\curriculums"
path_tesseract = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR"
poppler_path = r"C:\poppler\Library\bin"
save_path = r"C:\Users\pedro\Downloads\curriculums\images"
txt_save_path = r"C:\Users\pedro\Downloads\curriculums\txt_files"
pytesseract.pytesseract.tesseract_cmd = os.path.join(path_tesseract, "tesseract.exe")

keywords = ["Java", "Spring", "Python", "Django", "JavaScript", "React", "Node", 
            "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "HTML", "CSS", "Bootstrap"]

results = []

def convert_to_image(file_path, poppler_path, save_path):
    try:
        images = convert_from_path(file_path, poppler_path=poppler_path)
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(save_path, f"{os.path.basename(file_path)}_page_{i}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        return image_paths
    except Exception as e:
        logging.error(f"Erro ao converter PDF para imagens: {file_path} - {e}")
        return []

def extract_text(image_path):
    try:
        text = pytesseract.image_to_string(cv2.imread(image_path), lang="eng")
        return text
    except Exception as e:
        logging.error(f"Erro ao extrair texto da imagem: {image_path} - {e}")
        return ""

def extract_name_from_text(text):
    lines = text.splitlines()
    for line in lines[:2]:  # Analyse only the first two lines
        for name in line.split():
            if name.lower() in line.lower():
                return name
    return "Nome não encontrado"

def extract_contact(text):
    phone_pattern = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
    email_pattern = r'[a-zA-Z0-9._%+-]+\s?@\s?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    phones = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)
    
    return {
        "telefones": phones if phones else ["Telefone não encontrado"],
        "e-mails": emails if emails else ["E-mail não encontrado"]
    }

def extract_experience(text):
    experience_patterns = [
        r'(?P<cargo>[\w\s-]+)\n(?P<empresa>[\w\s]+)\s*\|\s*(?P<periodo>\d{4} - \d{4}|\d{4} - Presente|\d{4})',
        r'(?P<cargo>[\w\s-]+)\s*\|\s*(?P<empresa>[\w\s]+)\s*\|\s*(?P<periodo>\d{4} - \d{4}|\d{4} - Presente|\d{4})'
    ]
    
    experiences = []
    for pattern in experience_patterns:
        matches = re.finditer(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            experiences.append({
                "Cargo": match.group('cargo').strip(),
                "Empresa": match.group('empresa').strip(),
                "Período": match.group('periodo').strip()
            })

    return experiences if experiences else ["Nenhuma experiência identificada"]

def aproved(found_keywords):
    return len(found_keywords) > 5

def create_sheet(results):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Resultados"

        headers = ["Arquivo", "Nome", "Telefones", "E-mails", "Experiências", "Aprovado"]
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = openpyxl.styles.Font(bold=True)
            cell.alignment = openpyxl.styles.Alignment(horizontal="center")

        print("Inserindo dados na planilha...")
        for i, result in enumerate(results, start=2):
            if not isinstance(result, dict):
                logging.error(f"Formato inválido para o resultado: {result}")
                continue

            arquivo = result.get("Arquivo", "Desconhecido")
            name = result.get("Nome", "Nome não encontrado")
            telefones = result.get("Telefones", ["Telefone não encontrado"])
            emails = result.get("E-mails", ["E-mail não encontrado"])
            experiencias = result.get("Experiências", [])
            aprovado = result.get("Aprovado", False)

            ws[f"A{i}"] = arquivo
            ws[f"B{i}"] = name
            ws[f"C{i}"] = ", ".join(telefones)
            ws[f"D{i}"] = ", ".join(emails)
            ws[f"E{i}"] = "\n".join([f"{exp.get('Cargo', 'Desconhecido')} - "
                f"{exp.get('Empresa', 'Desconhecido')} - "
                f"{exp.get('Período', 'Desconhecido')}"
                    for exp in experiencias if isinstance(exp, dict)])
            ws[f"F{i}"].alignment = openpyxl.styles.Alignment(wrap_text=True)
            ws[f"F{i}"] = "Sim" if aprovado else "Não"

        print("Ajustando larguras das colunas...")
        for col in ws.columns:
            max_length = 0
            column = openpyxl.utils.get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column].width = max_length + 2

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        output_file = os.path.join(save_path, "resultados.xlsx")
        wb.save(output_file)
        print(f"Planilha de resultados criada com sucesso em {output_file}!")

    except Exception as e:
        logging.error(f"Erro ao criar planilha de resultados: {e}")
        print(f"Erro: {e}")

if not os.path.exists(save_path):
    os.makedirs(save_path)

if not os.path.exists(txt_save_path):
    os.makedirs(txt_save_path)

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        logging.info(f"Processando arquivo: {filename}")
        
        image_paths = convert_to_image(file_path, poppler_path, save_path)
        all_text = ""

        for image_path in image_paths:
            text = extract_text(image_path)
            all_text += text
            os.remove(image_path)
        
        txt_file_path = os.path.join(txt_save_path, f"{os.path.splitext(filename)[0]}.txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(all_text)

        name = extract_name_from_text(all_text)
        contact_info = extract_contact(all_text)
        experience_info = extract_experience(all_text)
        found_keywords = [kw for kw in keywords if kw.lower() in all_text.lower()]
        is_approved = aproved(found_keywords)

        results.append({
            "Arquivo": filename,
            "Nome": name,
            "Telefones": contact_info["telefones"],
            "E-mails": contact_info["e-mails"],
            "Experiências": experience_info,
            "Aprovado": is_approved
        })

create_sheet(results)
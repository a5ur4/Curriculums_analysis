import json
import os
import pytesseract
import cv2
import openpyxl
import re
import logging
import requests

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

experiences = []

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

def save_to_json(data, json_save_path, filename):
    try:
        json_file_path = os.path.join(json_save_path, f"{os.path.splitext(filename)[0]}.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Dados salvos em JSON: {json_file_path}")
    except Exception as e:
        logging.error(f"Erro ao salvar dados em JSON: {filename} - {e}")

def extract_name_from_text(text):
    lines = text.splitlines()
    for line in lines[:2]:
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
    experiences.clear()
    date_pattern = r'.*(20[0-2][0-9]|202[0-5]).*'

    lines = text.split('\n')
    for line in lines:
        if re.search(date_pattern, line):
            experiences.append(line.strip())
    
    unique_experiences = list(set(experiences))
    return unique_experiences

def aproved(found_keywords):
    return len(found_keywords) > 5

def create_sheet(results):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Resultados"

        headers = ["Arquivo", "Nome", "Telefones", "E-mails", "Aprovado", "Experiências"]
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
            ws[f"E{i}"].alignment = openpyxl.styles.Alignment(wrap_text=True)
            ws[f"E{i}"] = "Sim" if aprovado else "Não"
            ws[f"F{i}"] = "\n".join(experiencias)

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

# I think this is the best way to do this is seending all the extracted text to the LLM
# and writing a better prompt to get the best results using the keywords as a base
# and what the recruiter is looking for in the resume
def send_to_llm(data):
    url = "http://localhost:11434/api/generate" # Change this to the LLM API URL you are using
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3.2", # Change this to the model you are using
        "prompt": f"Analyze this resume data: {json.dumps(data)}",
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to LLM: {e}")
        return None

for result in results:
    llm_response = send_to_llm(result)
    if llm_response:
        logging.info(f"LLM response for {result['Arquivo']}: {llm_response}")

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
            save_to_json(text, txt_save_path, filename)
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

        result = {
            "Arquivo": filename,
            "Nome": name,
            "Telefones": contact_info["telefones"],
            "E-mails": contact_info["e-mails"],
            "Aprovado": is_approved,
            "Experiências": experience_info
        }

        results.append(result)

        llm_response = send_to_llm(result)
        if llm_response:
            logging.info(f"Resposta do LLM para {filename}: {llm_response}")

create_sheet(results)

#Made by: Pedro Bastos - a5ur4
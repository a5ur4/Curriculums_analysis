import os
import re
import pandas as pd
from pypdf import PdfReader

folder_path = r"C:\Users\pedro\Downloads\curriculums"

keywords = ["Java", "Spring", "Python", "Django", "JavaScript", "React", "Node", 
            "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "HTML", "CSS", "Bootstrap"]

results = []

def extract_contact(text):
    phone_pattern = r'\+?[\d\s()-]{10,15}' 
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    phones = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)
    
    return {
        "telefones": phones if phones else ["Telefone não encontrado"],
        "e-mails": emails if emails else ["E-mail não encontrado"]
    }

# Need to improve this function to extrect more information and to be more accurate
def extract_experience(text):
    experience_patterns = [
        r"(\d+\s+(anos|meses)\s+(de experiência|trabalhando))",
        r"(\b\d{4}\b\s*[-–]\s*\b\d{4}\b)",
        r"(\b\d{1,2}/\d{4}\b\s*[-–]\s*\b\d{1,2}/\d{4}\b)"
        # Add more patterns here
    ]
    
    role_patterns = [
        r"cargo[:\s]*([^\n,.;]+)",
        r"posição[:\s]*([^\n,.;]+)",
        r"função[:\s]*([^\n,.;]+)"
    ]

    time_matches = []
    for pattern in experience_patterns:
        time_matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    role_matches = []
    for pattern in role_patterns:
        role_matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    time_results = [match[0] if isinstance(match, tuple) else match for match in time_matches]
    roles_results = [match.strip() for match in role_matches]
    
    return {
        "tempos": time_results if time_results else ["Tempo de experiência não encontrado"],
        "funções": roles_results if roles_results else ["Função não encontrada"]
    }

def approved(found_keywords):
    return len(found_keywords) > 5

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        reader = PdfReader(file_path)
        all_text = ""
        
        for page in reader.pages:
            all_text += page.extract_text().lower()

        print(f"Analisando: {filename}")
        
        contact = extract_contact(all_text)
        experience = extract_experience(all_text)
        found_keywords = [keyword for keyword in keywords if keyword.lower() in all_text]
        is_approved = approved(found_keywords)

        results.append({
            "Arquivo": filename,
            "Telefones": ", ".join(contact["telefones"]),
            "E-mails": ", ".join(contact["e-mails"]),
            "Palavras-chave encontradas": ", ".join(found_keywords),
            "Quantidade de palavras-chave": len(found_keywords),
            "Tempos de experiência": ", ".join(experience["tempos"]),
            "Funções": ", ".join(experience["funções"]),
            "Aprovado": "Sim" if is_approved else "Não",
            "Páginas": len(reader.pages)
        })

output_file = "curriculums_analysis.xlsx"
df = pd.DataFrame(results)
df.to_excel(output_file, index=False)

print(f"Análise concluída! Resultados salvos em {output_file}")

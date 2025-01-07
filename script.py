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
        found_keywords = [keyword for keyword in keywords if keyword.lower() in all_text]
        is_approved = approved(found_keywords)

        results.append({
            "Arquivo": filename,
            "Telefones": ", ".join(contact["telefones"]),
            "E-mails": ", ".join(contact["e-mails"]),
            "Palavras-chave encontradas": ", ".join(found_keywords),
            "Quantidade de palavras-chave": len(found_keywords),
            "Aprovado": "Sim" if is_approved else "Não",
            "Páginas": len(reader.pages)
        })

output_file = "curriculums_analysis.xlsx"
df = pd.DataFrame(results)
df.to_excel(output_file, index=False)

print(f"Análise concluída! Resultados salvos em {output_file}")
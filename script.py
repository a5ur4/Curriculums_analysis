import os
import re
import pandas as pd
import pdfplumber

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

# This function still needs some improvements, but it's a good start
def extract_experience(text):
    experience_patterns = [
        r'(?P<cargo>[\w\s-]+)\n(?P<empresa>[\w\s]+)\s*\|\s*(?P<periodo>\d{4} - \d{4}|\d{4} - Presente|\d{4})',
        r'(?P<cargo>[\w\s-]+)\s*\|\s*(?P<empresa>[\w\s]+)\s*\|\s*(?P<periodo>\d{4} - \d{4}|\d{4} - Presente|\d{4})',
        r'(?P<cargo>[\w\s-]+)\n(?P<empresa>[\w\s]+)\s*\|\s*(?P<periodo>\d{4} - \d{4}|\d{4} - atual|\d{4})',
        r'(?P<cargo>[\w\s-]+)\s+at\s+(?P<empresa>[\w\s]+)\s*\((?P<periodo>[\d\s/-]+)\)'
    ]
    
    experiences = []
    for pattern in experience_patterns:
        matches = re.finditer(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            experiences.append({ # This append is not working as expected, need to make it go in other cells, and not just one
                "Cargo": match.group('cargo').strip(),
                "Empresa": match.group('empresa').strip(),
                "Período": match.group('periodo').strip()
            })

    return experiences if experiences else "Nenhuma experiência identificada"

def approved(found_keywords):
    return len(found_keywords) > 5

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        
        with pdfplumber.open(file_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() + "\n"
                print(all_text)

        print(f"Analisando: {filename}")
        
        contact = extract_contact(all_text)
        experiences = extract_experience(all_text)
        found_keywords = [keyword for keyword in keywords if keyword.lower() in all_text.lower()]
        is_approved = approved(found_keywords)

        results.append({
            "Arquivo": filename,
            "Telefones": ", ".join(contact["telefones"]),
            "E-mails": ", ".join(contact["e-mails"]),
            "Palavras-chave encontradas": ", ".join(found_keywords),
            "Quantidade de palavras-chave": len(found_keywords),
            # Divide the experiences in different columns and cells
            "Experiências": experiences if isinstance(experiences, str) else pd.json_normalize(experiences).to_string(index=False),
            "Aprovado": "Sim" if is_approved else "Não"
        })

output_file = "curriculums_analysis.xlsx"
df = pd.DataFrame(results)
df.to_excel(output_file, index=False)

print(f"Análise concluída! Resultados salvos em {output_file}")

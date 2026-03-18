import PyPDF2
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    """
    Extrai texto de um PDF do LinkedIn
    
    Args:
        uploaded_file: Arquivo PDF uploadado via Streamlit
        
    Returns:
        str: Texto extraído do PDF
    """
    try:
        # Criar objeto BytesIO do arquivo
        pdf_file = BytesIO(uploaded_file.read())
        
        # Criar leitor de PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extrair texto de todas as páginas
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Limpar texto
        text = text.strip()
        
        return text
    
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

def clean_linkedin_text(text):
    """
    Limpa e organiza o texto extraído do LinkedIn
    
    Args:
        text: Texto bruto do PDF
        
    Returns:
        str: Texto limpo e organizado
    """
    # Remove linhas vazias múltiplas
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Junta de volta
    cleaned_text = '\n'.join(lines)
    
    return cleaned_text

def extract_sections(text):
    """
    Tenta identificar seções principais do perfil LinkedIn
    
    Args:
        text: Texto do PDF
        
    Returns:
        dict: Dicionário com seções identificadas
    """
    sections = {
        'headline': '',
        'about': '',
        'experience': '',
        'education': '',
        'skills': '',
        'full_text': text
    }
    
    # Marcadores comuns em PDFs do LinkedIn
    markers = {
        'about': ['Sobre', 'About', 'Summary', 'Resumo'],
        'experience': ['Experiência', 'Experience', 'Experiencia'],
        'education': ['Formação acadêmica', 'Education', 'Educação', 'Educacao'],
        'skills': ['Competências', 'Skills', 'Habilidades']
    }
    
    # Tentativa simples de extração por marcadores
    text_lower = text.lower()
    
    for section, keywords in markers.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                # Encontrar índice do marcador
                idx = text_lower.index(keyword.lower())
                # Extrair próximos 1000 caracteres como seção
                sections[section] = text[idx:idx+1000]
                break
    
    return sections

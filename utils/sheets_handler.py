import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

def save_lead_to_sheets(name, email):
    """
    Salva lead no Google Sheets
    
    Args:
        name: Nome do usuário
        email: Email do usuário
    """
    
    try:
        # Verificar se existe credentials no Streamlit secrets
        if hasattr(__import__('streamlit'), 'secrets'):
            import streamlit as st
            
            if 'gcp_service_account' in st.secrets:
                # Usar credentials do Streamlit secrets
                credentials_dict = dict(st.secrets['gcp_service_account'])
                
                # Definir scopes
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                
                # Criar credentials
                credentials = Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=scopes
                )
                
                # Autorizar gspread
                gc = gspread.authorize(credentials)
                
                # Abrir planilha (você vai precisar compartilhar com o service account)
                sheet_url = st.secrets.get('google_sheet_url', '')
                
                if sheet_url:
                    # Abrir por URL
                    spreadsheet = gc.open_by_url(sheet_url)
                    worksheet = spreadsheet.sheet1
                    
                    # Adicionar linha com timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    worksheet.append_row([timestamp, name, email])
                    
                    return True
                else:
                    # Se não tem URL, tenta criar ou abrir planilha padrão
                    try:
                        spreadsheet = gc.open('LinkedPro Leads')
                    except:
                        # Criar nova planilha
                        spreadsheet = gc.create('LinkedPro Leads')
                        spreadsheet.share('', perm_type='anyone', role='reader')
                    
                    worksheet = spreadsheet.sheet1
                    
                    # Adicionar header se vazio
                    if worksheet.row_count == 0:
                        worksheet.append_row(['Timestamp', 'Nome', 'Email'])
                    
                    # Adicionar lead
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    worksheet.append_row([timestamp, name, email])
                    
                    return True
            else:
                # Sem credentials configuradas
                print("Google Sheets não configurado - lead não salvo")
                return False
        else:
            # Streamlit secrets não disponível
            return False
            
    except Exception as e:
        print(f"Erro ao salvar lead: {str(e)}")
        # Não falhar a aplicação por causa disso
        return False

def setup_google_sheets():
    """
    Função helper para configurar Google Sheets
    Retorna instruções de setup
    """
    
    instructions = """
    # Como configurar Google Sheets para salvar leads:
    
    1. Acesse: https://console.cloud.google.com/
    
    2. Crie um novo projeto (ou use existente)
    
    3. Ative as APIs:
       - Google Sheets API
       - Google Drive API
    
    4. Crie credenciais:
       - Vá em "Credenciais"
       - Criar credenciais → Conta de serviço
       - Baixe o JSON da service account
    
    5. No Streamlit Cloud:
       - Vá em Settings → Secrets
       - Cole o conteúdo do JSON assim:
       
       [gcp_service_account]
       type = "service_account"
       project_id = "seu-projeto"
       private_key_id = "..."
       private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
       client_email = "..."
       client_id = "..."
       auth_uri = "https://accounts.google.com/o/oauth2/auth"
       token_uri = "https://oauth2.googleapis.com/token"
       auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
       client_x509_cert_url = "..."
       
    6. Crie uma planilha no Google Sheets chamada "LinkedPro Leads"
    
    7. Compartilhe a planilha com o email da service account (client_email do JSON)
       com permissão de Editor
    
    8. (Opcional) Adicione a URL da planilha nos secrets:
       google_sheet_url = "https://docs.google.com/spreadsheets/d/..."
    
    Pronto! Os leads serão salvos automaticamente.
    """
    
    return instructions

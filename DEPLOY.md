# 🚀 GUIA RÁPIDO DE DEPLOY - 5 MINUTOS

## Opção 1: Deploy Direto (Mais Rápido)

### 1. Prepare o GitHub

```bash
# No seu terminal, na pasta do projeto:
git init
git add .
git commit -m "LinkedPro Analyzer - Initial commit"
git branch -M main
```

### 2. Crie o Repositório no GitHub

1. Vá em https://github.com/new
2. Nome: `linkedpro-analyzer` (ou outro nome)
3. **NÃO** marque "Initialize with README"
4. Clique em "Create repository"

### 3. Faça Push

```bash
# Substitua SEU-USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU-USUARIO/linkedpro-analyzer.git
git push -u origin main
```

### 4. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique em "New app"
3. Faça login com GitHub
4. Preencha:
   - **Repository:** seu-usuario/linkedpro-analyzer
   - **Branch:** main
   - **Main file path:** app.py
5. Clique em "Deploy!"

**🎉 PRONTO! Seu app está no ar!**

A URL será algo como: `https://seu-app.streamlit.app`

---

## Opção 2: Testar Localmente Primeiro

### Linux/Mac:

```bash
chmod +x run_local.sh
./run_local.sh
```

### Windows:

```bash
run_local.bat
```

Acesse: http://localhost:8501

---

## ⚙️ Configurações Opcionais (Depois do Deploy)

### Adicionar Google Sheets (Salvar Leads)

#### Passo 1: Google Cloud Console

1. Vá em https://console.cloud.google.com/
2. Crie um projeto novo
3. Ative as APIs:
   - Google Sheets API
   - Google Drive API
4. Crie uma Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Nome: "linkedpro-sheets"
   - Role: Editor
   - Create Key → JSON → Baixe o arquivo

#### Passo 2: Google Sheets

1. Crie uma planilha: "LinkedPro Leads"
2. Primeira linha (headers):
   - A1: Timestamp
   - B1: Nome
   - C1: Email
3. Compartilhe com o email da service account (está no JSON)
   - Permissão: Editor

#### Passo 3: Streamlit Secrets

1. No Streamlit Cloud, seu app → Settings → Secrets
2. Cole (substitua com seus dados do JSON):

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "linkedpro-sheets@seu-projeto.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."

google_sheet_url = "https://docs.google.com/spreadsheets/d/SUA_PLANILHA/edit"
```

3. Clique em Save
4. App vai reiniciar

**✅ Leads agora são salvos automaticamente!**

---

## 🎯 Como Usar o App

### Para Seus Usuários:

1. Abrir a URL do app
2. Preencher nome e email
3. Baixar PDF do LinkedIn:
   - linkedin.com/in/seu-perfil
   - Mais → Salvar como PDF
4. Upload do PDF
5. Conseguir Groq API Key:
   - console.groq.com
   - Create API Key (grátis!)
6. Analisar!

### Para Você:

- Ver leads na planilha Google Sheets
- Monitorar uso no Streamlit Cloud (Settings → Analytics)
- Compartilhar a URL nas redes sociais

---

## ❓ Problemas Comuns

**"Module not found"**
- Certifique-se que requirements.txt está no repositório
- Streamlit Cloud instala automaticamente

**"API Key inválida"**
- Groq key começa com `gsk_`
- Pegue em console.groq.com

**"Não salva leads"**
- Não configurou Google Sheets? Tudo bem, funciona sem
- Quer configurar? Siga o guia acima

**"App lento"**
- Groq é muito rápido (5-10s)
- Se usar OpenAI, demora mais (30-60s)

---

## 📊 Próximos Passos

1. ✅ Deploy básico funcionando
2. ⬜ Configurar Google Sheets
3. ⬜ Compartilhar nas redes
4. ⬜ Coletar feedback
5. ⬜ Iterar e melhorar

---

**Qualquer dúvida, abra uma issue no GitHub ou me envie mensagem!**

🚀 Boa sorte com seu LinkedPro Analyzer!

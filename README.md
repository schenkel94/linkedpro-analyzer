# 🚀 LinkedPro Analyzer

Análise profissional **100% GRATUITA** de perfis LinkedIn usando IA.

## ✨ Funcionalidades

- ✅ Análise completa em 7 dimensões
- ✅ Score detalhado (0-100) por categoria
- ✅ Sugestões personalizadas de melhoria
- ✅ Reescrita profissional de headline e resumo
- ✅ Checklist priorizado de ações
- ✅ Download do resultado em Markdown
- ✅ Captura automática de leads
- ✅ 100% gratuito para o usuário

## 🛠️ Stack Tecnológica

- **Frontend:** Streamlit
- **IA:** Groq API (Llama 3.1 70B) ou OpenAI GPT-4
- **Leads:** Google Sheets
- **Deploy:** Streamlit Cloud (gratuito)
- **Custo:** R$ 0,00/mês

## 📋 Pré-requisitos

1. Conta no GitHub
2. Conta no Streamlit Cloud (gratuita)
3. API Key da Groq (gratuita) ou OpenAI
4. (Opcional) Google Cloud Project para salvar leads

## 🚀 Deploy Rápido (5 minutos)

### Passo 1: Preparar o Repositório

1. Crie um novo repositório no GitHub
2. Clone este código
3. Faça push para o GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione:
   - **Repository:** seu-usuario/seu-repo
   - **Branch:** main
   - **Main file path:** app.py
5. Clique em "Deploy!"

**Pronto! Seu app já está no ar!** 🎉

### Passo 3: (Opcional) Configurar Google Sheets para Leads

#### 3.1. Criar Service Account

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto (ou use existente)
3. Ative as APIs:
   - Google Sheets API
   - Google Drive API
4. Vá em **IAM & Admin** → **Service Accounts**
5. Clique em **Create Service Account**
   - Nome: "linkedpro-sheets"
   - Clique em "Create and Continue"
   - Role: "Editor"
   - Clique em "Done"
6. Clique na service account criada
7. Vá em **Keys** → **Add Key** → **Create new key**
8. Escolha **JSON** e baixe o arquivo

#### 3.2. Criar Planilha Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com)
2. Crie uma nova planilha chamada "LinkedPro Leads"
3. Na primeira linha, adicione os headers:
   - A1: Timestamp
   - B1: Nome
   - C1: Email
4. Clique em **Compartilhar**
5. Cole o email da service account (está no JSON, campo `client_email`)
6. Dê permissão de **Editor**
7. Copie a URL da planilha

#### 3.3. Configurar Secrets no Streamlit

1. No Streamlit Cloud, vá no seu app
2. Clique em **Settings** → **Secrets**
3. Cole o seguinte (ajuste com seus dados do JSON):

```toml
# Google Service Account
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "linkedpro-sheets@seu-projeto.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

# URL da Planilha (opcional, mas recomendado)
google_sheet_url = "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit"
```

4. Clique em **Save**
5. O app vai reiniciar automaticamente

**Atenção:** A `private_key` deve ter `\n` no final de cada linha. Exemplo:
```
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n...sua chave...\n-----END PRIVATE KEY-----\n"
```

## 🔑 Como Conseguir API Keys

### Groq API (Recomendado - 100% Grátis)

1. Acesse [console.groq.com](https://console.groq.com)
2. Faça login com Google/GitHub
3. Vá em **API Keys**
4. Clique em **Create API Key**
5. Copie a chave (começa com `gsk_...`)

**Vantagens:**
- ✅ Totalmente gratuito
- ✅ Super rápido (600+ tokens/s)
- ✅ Sem necessidade de cartão de crédito
- ✅ Rate limit generoso

### OpenAI API (Alternativa)

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta
3. Vá em **API Keys**
4. Crie uma nova chave
5. Adicione créditos (pago)

## 📊 Estrutura do Projeto

```
linkedin-analyzer/
├── app.py                      # Aplicação principal
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py          # Extração de texto do PDF
│   ├── linkedin_analyzer.py   # Análise com IA
│   └── sheets_handler.py      # Salvamento de leads
├── .streamlit/
│   └── config.toml            # Configurações do Streamlit
├── requirements.txt           # Dependências Python
├── .gitignore
└── README.md
```

## 🎯 Como Usar

### Para Usuários Finais:

1. Acesse o app
2. Preencha nome e email
3. Baixe o PDF do seu perfil LinkedIn:
   - Acesse seu perfil
   - Clique em "Mais"
   - "Salvar como PDF"
4. Faça upload do PDF
5. Cole sua Groq API Key (grátis!)
6. Clique em "Analisar"
7. Receba análise completa em 30-60 segundos
8. Baixe o resultado

### Para Você (Admin):

1. Acesse a planilha Google Sheets para ver os leads
2. Exporte para CSV e importe no seu CRM
3. Configure automações de email marketing
4. Monitore quantas pessoas estão usando

## 🔧 Customização

### Mudar Cores/Design

Edite `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#ff6b35"  # Cor principal
backgroundColor="#0f0f1e"  # Fundo
secondaryBackgroundColor="#1a1a2e"  # Fundo secundário
textColor="#e8e8e8"  # Texto
```

### Adicionar Mais Dimensões de Análise

Edite `utils/linkedin_analyzer.py` no prompt `analysis_prompt`.

### Mudar Modelo de IA

No `utils/linkedin_analyzer.py`, linha ~50:

```python
"model": "llama-3.1-70b-versatile",  # Groq
# Ou
"model": "gpt-4",  # OpenAI
```

## 📈 Métricas e Analytics

O app não tem analytics built-in, mas você pode adicionar:

1. **Google Analytics:** Adicione o script no `app.py`
2. **Streamlit Analytics:** Ative nas configurações do Streamlit Cloud
3. **Google Sheets:** Contagem automática de linhas = número de leads

## 🐛 Troubleshooting

### Erro: "API Key inválida"
- Verifique se copiou a key completa
- Para Groq, deve começar com `gsk_`
- Para OpenAI, deve começar com `sk-`

### Erro: "Não consegue ler o PDF"
- Certifique-se que é o PDF do LinkedIn
- Tente baixar o PDF novamente
- Arquivo deve ser menor que 200MB

### Leads não salvam no Google Sheets
- Verifique se configurou os secrets corretamente
- Confirme que compartilhou a planilha com a service account
- Veja logs no Streamlit Cloud: Settings → Logs

### App está lento
- Groq é muito rápido (~5s)
- OpenAI pode demorar 30-60s
- Verifique sua conexão de internet

## 💡 Ideias de Melhoria

- [ ] Adicionar análise de foto de perfil
- [ ] Comparação com perfis top da indústria
- [ ] Sugestões de posts para aumentar engajamento
- [ ] Exportar para PDF formatado
- [ ] Email automático com resultado
- [ ] Versão em inglês
- [ ] Análise de concorrentes
- [ ] Integração com LinkedIn API
- [ ] Modo "antes e depois"
- [ ] Score board público

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar!

## 🤝 Contribuições

Pull requests são bem-vindos! Para mudanças grandes, abra uma issue primeiro.

## 📧 Contato

Dúvidas? Abra uma issue no GitHub!

---

**Feito com ❤️ usando IA**

*Promova esta ferramenta gratuitamente e ajude profissionais a melhorarem seus perfis!*

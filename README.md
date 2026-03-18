# 🚀 LinkedPro Analyzer

Análise profissional **100% GRATUITA** de perfis LinkedIn usando IA.

## ✨ Funcionalidades

- ✅ Análise completa em 7 dimensões
- ✅ Score detalhado (0-100) por categoria
- ✅ Sugestões personalizadas de melhoria
- ✅ Reescrita profissional de headline e resumo
- ✅ Checklist priorizado de ações
- ✅ Download do resultado em Markdown
- ✅ 100% gratuito - sem cadastro necessário
- ✅ Rápido: análise completa em ~15 segundos

## 🛠️ Stack Tecnológica

- **Frontend:** Streamlit
- **IA:** Groq API (Llama 3.1 70B) - Super rápido!
- **Deploy:** Streamlit Cloud (gratuito)
- **Custo:** R$ 0,00/mês

## 🚀 Deploy Rápido (3 minutos)

### Passo 1: Preparar o Repositório

1. Crie um novo repositório no GitHub
2. Clone este código
3. **IMPORTANTE:** Edite `app.py` linha 8 e substitua pela sua API key do Groq

```python
# Linha 8 do app.py
GROQ_API_KEY = "sua_api_key_aqui"
```

### Como conseguir Groq API Key (GRÁTIS):

1. Acesse [console.groq.com](https://console.groq.com)
2. Faça login com Google/GitHub
3. Vá em "API Keys"
4. Crie uma nova key
5. Copie e cole no `app.py`

### Passo 2: Fazer Push para GitHub

```bash
git init
git add .
git commit -m "LinkedPro Analyzer"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/linkedpro-analyzer.git
git push -u origin main
```

### Passo 3: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione:
   - **Repository:** seu-usuario/linkedpro-analyzer
   - **Branch:** main
   - **Main file path:** app.py
5. Clique em "Deploy!"

**🎉 PRONTO! Seu app está no ar!**

A URL será algo como: `https://linkedpro-analyzer.streamlit.app`

## 📋 Estrutura do Projeto

```
linkedin-analyzer/
├── app.py                      # Aplicação principal ⭐
├── utils/
│   ├── pdf_parser.py          # Extração de texto do PDF
│   ├── linkedin_analyzer.py   # Análise com IA (Groq)
│   └── sheets_handler.py      # (não usado - pode deletar)
├── .streamlit/
│   └── config.toml            # Configurações do Streamlit
├── requirements.txt           # Dependências Python
└── README.md
```

## 🎯 Como Usar

### Para Usuários Finais:

1. Acesse o app
2. Baixe o PDF do seu perfil LinkedIn:
   - Acesse seu perfil
   - Clique em "Mais"
   - "Salvar como PDF"
3. Faça upload do PDF
4. Clique em "Analisar"
5. Receba análise completa em 15 segundos
6. Baixe o resultado

### Para Você (Admin):

- O app está 100% funcional e gratuito
- Você paga $0 por mês (Streamlit Cloud é grátis)
- Groq API é gratuita
- Sem necessidade de banco de dados ou autenticação

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

Edite `utils/linkedin_analyzer.py` no prompt `analysis_prompt` (linha ~20).

### Mudar Modelo de IA

No `utils/linkedin_analyzer.py`, linha ~100:

```python
"model": "llama-3.1-70b-versatile",  # Groq - Atual
# Outros modelos disponíveis:
# "llama-3.3-70b-versatile"
# "llama-3.1-8b-instant"
# "mixtral-8x7b-32768"
```

## 🐛 Troubleshooting

### Erro: "API Key inválida"
- Verifique se copiou a key completa do Groq
- Deve começar com `gsk_`
- Edite o arquivo `app.py` linha 8

### Erro: "Não consegue ler o PDF"
- Certifique-se que é o PDF do LinkedIn
- Tente baixar o PDF novamente
- Arquivo deve ser menor que 200MB

### App está lento
- Groq é muito rápido (~10-15s)
- Se estiver demorando mais, pode ser a internet
- Ou muitos usuários simultâneos (rate limit do Groq)

## 💡 Ideias de Melhoria

- [ ] Adicionar análise de foto de perfil
- [ ] Comparação com perfis top da indústria
- [ ] Sugestões de posts para aumentar engajamento
- [ ] Exportar para PDF formatado
- [ ] Versão em inglês
- [ ] Modo "antes e depois"
- [ ] Analytics (quantas pessoas usaram)

## 🔒 Segurança

**IMPORTANTE:** Nunca commite sua API key no GitHub público!

Se você acidentalmente commitou sua API key:
1. Delete a key no console do Groq
2. Crie uma nova
3. Use `git filter-branch` para remover do histórico

**Dica:** Use Streamlit Secrets para produção:
1. No Streamlit Cloud → Settings → Secrets
2. Adicione: `GROQ_API_KEY = "sua_key"`
3. No código: `os.environ.get("GROQ_API_KEY")`

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar!

## 🤝 Contribuições

Pull requests são bem-vindos!

## 📧 Contato

Dúvidas? Abra uma issue no GitHub!

---

**Feito com ❤️ usando IA**

*Promova esta ferramenta gratuitamente e ajude profissionais a melhorarem seus perfis!*

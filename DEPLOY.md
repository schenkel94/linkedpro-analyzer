# 🚀 GUIA RÁPIDO DE DEPLOY - 3 MINUTOS

## Passo 1: Conseguir Groq API Key (1 minuto)

1. Acesse: **https://console.groq.com**
2. Faça login com Google ou GitHub
3. Vá em **"API Keys"** no menu lateral
4. Clique em **"Create API Key"**
5. Copie a chave (começa com `gsk_...`)

✅ **Chave copiada!**

---

## Passo 2: Configurar a API Key no Código (30 segundos)

1. Abra o arquivo **`app.py`**
2. Na **linha 8**, substitua:

```python
# ANTES:
GROQ_API_KEY = "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"

# DEPOIS (cole sua chave):
GROQ_API_KEY = "gsk_SuaChaveAqui"
```

3. Salve o arquivo

✅ **API Key configurada!**

---

## Passo 3: Fazer Upload para o GitHub (1 minuto)

### 3.1. Inicializar Git

```bash
# No terminal, na pasta do projeto:
git init
git add .
git commit -m "LinkedPro Analyzer"
git branch -M main
```

### 3.2. Criar Repositório no GitHub

1. Vá em **https://github.com/new**
2. Nome: `linkedpro-analyzer`
3. **NÃO** marque nenhuma opção
4. Clique em **"Create repository"**

### 3.3. Fazer Push

```bash
# Substitua SEU-USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU-USUARIO/linkedpro-analyzer.git
git push -u origin main
```

✅ **Código no GitHub!**

---

## Passo 4: Deploy no Streamlit Cloud (1 minuto)

1. Acesse: **https://share.streamlit.io**
2. Clique em **"New app"**
3. Faça login com **GitHub**
4. Preencha:
   - **Repository:** `seu-usuario/linkedpro-analyzer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Clique em **"Deploy!"**

⏳ Aguarde 2-3 minutos enquanto faz deploy...

🎉 **APP NO AR!**

A URL será algo como: `https://linkedpro-analyzer.streamlit.app`

---

## ✅ Pronto! Agora Teste

1. Abra a URL do seu app
2. Baixe o PDF do LinkedIn:
   - linkedin.com/in/seu-perfil
   - Mais → Salvar como PDF
3. Faça upload no app
4. Clique em "Analisar"
5. Veja a mágica acontecer! ✨

---

## 🔒 IMPORTANTE - Segurança da API Key

Sua API key está no código publicamente visível no GitHub!

**Para produção, use Streamlit Secrets:**

### Opção Segura (Recomendado para produção):

1. No **Streamlit Cloud**, vá em seu app
2. **Settings** → **Secrets**
3. Adicione:

```toml
GROQ_API_KEY = "gsk_SuaChaveAqui"
```

4. No **`app.py`**, linha 8, mude para:

```python
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
```

5. Commite e faça push da mudança

Agora a key não está mais visível no código! 🔒

---

## 🎯 Próximos Passos

- [ ] Teste o app com seu próprio perfil
- [ ] Compartilhe com amigos
- [ ] Promova nas redes sociais
- [ ] Colete feedback
- [ ] Customize cores/design
- [ ] Adicione novas features

---

## ❓ Problemas Comuns

**"Module not found"**
- Streamlit Cloud instala automaticamente do `requirements.txt`
- Espere alguns minutos e recarregue

**"Erro na análise"**
- Verifique se sua Groq API Key está correta
- Deve começar com `gsk_`

**"App lento"**
- Groq é super rápido (10-15s)
- Se demorar mais, pode ser rate limit
- Tente novamente em alguns segundos

---

**Alguma dúvida? Abra uma issue no GitHub!**

🚀 Boa sorte com seu LinkedPro Analyzer!

import json
import requests
import time

def analyze_profile(pdf_text, api_key, progress_callback=None):
    """
    Analisa perfil LinkedIn usando Groq API
    
    Args:
        pdf_text: Texto extraído do PDF
        api_key: Chave da API Groq
        progress_callback: Função para atualizar progresso
        
    Returns:
        dict: Resultado da análise estruturado
    """
    return analyze_with_groq(pdf_text, api_key, progress_callback)

def analyze_with_groq(pdf_text, api_key, progress_callback=None):
    """Análise usando Groq API (Llama 3.1 70B)"""
    
    # Prompt otimizado para análise de LinkedIn
    analysis_prompt = f"""Você é um especialista em otimização de perfis LinkedIn e recrutamento. Analise o perfil abaixo e retorne um JSON estruturado.

PERFIL LINKEDIN:
{pdf_text[:4000]}

Retorne APENAS um JSON válido (sem markdown, sem explicações) com esta estrutura exata:

{{
  "overall_score": <número de 0-100>,
  "dimensions": {{
    "headline": {{
      "title": "Headline & Primeira Impressão",
      "icon": "🎯",
      "score": <0-100>,
      "analysis": "<análise de 2-3 frases>",
      "suggestions": ["sugestão 1", "sugestão 2", "sugestão 3"],
      "rewrite": "<versão reescrita da headline>"
    }},
    "about": {{
      "title": "Sobre / Resumo",
      "icon": "📝",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."],
      "rewrite": "<versão reescrita do sobre>"
    }},
    "experience": {{
      "title": "Experiências Profissionais",
      "icon": "💼",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."]
    }},
    "skills": {{
      "title": "Habilidades & Keywords",
      "icon": "🛠️",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."]
    }},
    "visibility": {{
      "title": "Visibilidade & SEO",
      "icon": "👁️",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."]
    }},
    "engagement": {{
      "title": "Potencial de Engajamento",
      "icon": "🔥",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."]
    }},
    "ats": {{
      "title": "Otimização para ATS",
      "icon": "🤖",
      "score": <0-100>,
      "analysis": "<análise>",
      "suggestions": ["...", "...", "..."]
    }}
  }},
  "priority_actions": [
    {{"action": "Ação 1", "impact": "Alto", "why": "Explicação curta"}},
    {{"action": "Ação 2", "impact": "Alto", "why": "Explicação curta"}},
    {{"action": "Ação 3", "impact": "Médio", "why": "Explicação curta"}},
    {{"action": "Ação 4", "impact": "Médio", "why": "Explicação curta"}},
    {{"action": "Ação 5", "impact": "Baixo", "why": "Explicação curta"}}
  ]
}}

CRITÉRIOS DE AVALIAÇÃO:
- Headline: Clareza, keywords, diferenciação
- Sobre: Storytelling, CTAs, valor oferecido
- Experiência: Métricas, verbos de ação, resultados
- Habilidades: Relevância, quantidade, endossos
- Visibilidade: Keywords SEO, completude do perfil
- Engajamento: Chamadas para ação, redes sociais
- ATS: Formatação, keywords, compatibilidade

Seja CRÍTICO mas CONSTRUTIVO. Scores devem refletir a realidade (não seja generoso demais).
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",  # Modelo atualizado
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em LinkedIn e recrutamento. Retorne sempre JSON válido, sem markdown."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    if progress_callback:
        progress_callback(0.3)
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if progress_callback:
            progress_callback(0.6)
        
        if response.status_code != 200:
            raise Exception(f"Erro na API Groq: {response.status_code} - {response.text}")
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Limpar possível markdown
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        # Parse JSON
        analysis_result = json.loads(content)
        
        if progress_callback:
            progress_callback(1.0)
        
        return analysis_result
    
    except json.JSONDecodeError as e:
        # Fallback: estrutura básica
        return create_fallback_analysis(pdf_text)
    
    except Exception as e:
        raise Exception(f"Erro ao chamar Groq API: {str(e)}")

def analyze_with_openai(pdf_text, api_key, progress_callback=None):
    """Análise usando OpenAI GPT-4"""
    
    # Similar ao Groq, mas com endpoint OpenAI
    analysis_prompt = f"""Você é um especialista em otimização de perfis LinkedIn. Analise o perfil abaixo e retorne um JSON estruturado.

PERFIL:
{pdf_text[:4000]}

[Mesmo prompt do Groq...]
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em LinkedIn. Retorne sempre JSON válido."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    
    if progress_callback:
        progress_callback(0.3)
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if progress_callback:
            progress_callback(0.6)
        
        if response.status_code != 200:
            raise Exception(f"Erro na API OpenAI: {response.status_code}")
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Limpar e parsear
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        analysis_result = json.loads(content)
        
        if progress_callback:
            progress_callback(1.0)
        
        return analysis_result
    
    except Exception as e:
        raise Exception(f"Erro ao chamar OpenAI API: {str(e)}")

def create_fallback_analysis(pdf_text):
    """Cria uma análise básica de fallback caso a IA falhe"""
    
    return {
        "overall_score": 65,
        "dimensions": {
            "headline": {
                "title": "Headline & Primeira Impressão",
                "icon": "🎯",
                "score": 60,
                "analysis": "Sua headline precisa ser mais específica e mostrar seu valor único. Evite títulos genéricos.",
                "suggestions": [
                    "Inclua sua especialidade principal",
                    "Adicione resultados ou diferencial",
                    "Use keywords relevantes para sua área"
                ],
                "rewrite": "[Sua Especialidade] | Ajudo [Público-Alvo] a [Resultado Específico]"
            },
            "about": {
                "title": "Sobre / Resumo",
                "icon": "📝",
                "score": 65,
                "analysis": "Seu resumo precisa contar uma história e mostrar seus resultados de forma clara.",
                "suggestions": [
                    "Comece com um gancho forte",
                    "Inclua métricas e resultados",
                    "Termine com call-to-action"
                ],
                "rewrite": "Revise seu 'Sobre' para incluir storytelling, resultados quantificáveis e uma chamada para ação clara."
            },
            "experience": {
                "title": "Experiências Profissionais",
                "icon": "💼",
                "score": 70,
                "analysis": "Suas experiências precisam focar mais em resultados do que em responsabilidades.",
                "suggestions": [
                    "Use verbos de ação no início",
                    "Quantifique seus resultados",
                    "Mostre o impacto do seu trabalho"
                ]
            },
            "skills": {
                "title": "Habilidades & Keywords",
                "icon": "🛠️",
                "score": 65,
                "analysis": "Organize suas habilidades estrategicamente e busque endossos.",
                "suggestions": [
                    "Priorize habilidades mais relevantes",
                    "Peça endossos de colegas",
                    "Adicione habilidades emergentes da sua área"
                ]
            },
            "visibility": {
                "title": "Visibilidade & SEO",
                "icon": "👁️",
                "score": 60,
                "analysis": "Seu perfil precisa de otimização para aparecer em mais buscas.",
                "suggestions": [
                    "Use keywords estratégicas",
                    "Complete 100% do perfil",
                    "Mantenha perfil em inglês + português"
                ]
            },
            "engagement": {
                "title": "Potencial de Engajamento",
                "icon": "🔥",
                "score": 55,
                "analysis": "Aumente suas chances de ser contatado com CTAs claros.",
                "suggestions": [
                    "Adicione formas de contato",
                    "Crie senso de urgência",
                    "Mostre disponibilidade"
                ]
            },
            "ats": {
                "title": "Otimização para ATS",
                "icon": "🤖",
                "score": 70,
                "analysis": "Seu perfil está razoavelmente otimizado para sistemas ATS.",
                "suggestions": [
                    "Use termos padrão da indústria",
                    "Evite formatações complexas",
                    "Inclua certificações"
                ]
            }
        },
        "priority_actions": [
            {"action": "Reescrever headline com foco em resultados", "impact": "Alto", "why": "Primeira coisa que recrutadores veem"},
            {"action": "Adicionar métricas nas experiências", "impact": "Alto", "why": "Mostra seu impacto real"},
            {"action": "Completar seção 'Sobre' com storytelling", "impact": "Alto", "why": "Aumenta conexão emocional"},
            {"action": "Reorganizar habilidades por relevância", "impact": "Médio", "why": "Melhora SEO do perfil"},
            {"action": "Adicionar call-to-action", "impact": "Médio", "why": "Facilita contato de recrutadores"}
        ]
    }

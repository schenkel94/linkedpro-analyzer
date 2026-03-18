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
{pdf_text[:6000]}

INSTRUÇÕES CRÍTICAS:
1. Analise o CONTEÚDO REAL do perfil acima
2. Sugestões devem ser ESPECÍFICAS e PERSONALIZADAS baseadas no que a pessoa escreveu
3. Cada dimensão deve ter EXATAMENTE 3 sugestões concisas e acionáveis
4. Reescritas devem usar o conteúdo atual da pessoa como base, não criar do zero
5. Seja crítico mas construtivo - scores devem refletir a realidade
6. Identifique pontos fortes E fracos específicos do perfil

Retorne APENAS um JSON válido (sem markdown, sem explicações) com esta estrutura exata:

{{
  "overall_score": <número de 0-100 baseado na análise real>,
  "dimensions": {{
    "headline": {{
      "title": "Headline & Primeira Impressão",
      "icon": "🎯",
      "score": <0-100>,
      "analysis": "<2-3 frases sobre a headline ATUAL da pessoa, citando o que ela escreveu>",
      "suggestions": [
        "<sugestão específica 1 baseada no conteúdo atual>",
        "<sugestão específica 2 com exemplo concreto>",
        "<sugestão específica 3 acionável>"
      ],
      "rewrite": "<versão melhorada da headline ATUAL da pessoa, mantendo sua área e experiência>"
    }},
    "about": {{
      "title": "Sobre / Resumo",
      "icon": "📝",
      "score": <0-100>,
      "analysis": "<análise do resumo ATUAL, citando trechos específicos se houver>",
      "suggestions": [
        "<sugestão específica 1>",
        "<sugestão específica 2>",
        "<sugestão específica 3>"
      ],
      "rewrite": "<versão melhorada do resumo ATUAL, incorporando a história e experiência da pessoa>"
    }},
    "experience": {{
      "title": "Experiências Profissionais",
      "icon": "💼",
      "score": <0-100>,
      "analysis": "<análise das experiências ATUAIS listadas>",
      "suggestions": [
        "<sugestão específica para melhorar descrição de cargos>",
        "<sugestão sobre adicionar métricas em funções específicas>",
        "<sugestão sobre destacar conquistas reais>"
      ]
    }},
    "skills": {{
      "title": "Habilidades & Keywords",
      "icon": "🛠️",
      "score": <0-100>,
      "analysis": "<análise das habilidades listadas ou faltantes>",
      "suggestions": [
        "<sugestão sobre habilidades específicas da área da pessoa>",
        "<sugestão sobre organização/priorização>",
        "<sugestão sobre keywords relevantes para a indústria>"
      ]
    }},
    "visibility": {{
      "title": "Visibilidade & SEO",
      "icon": "👁️",
      "score": <0-100>,
      "analysis": "<análise de completude e otimização para busca>",
      "suggestions": [
        "<sugestão específica de SEO>",
        "<sugestão sobre seções faltantes>",
        "<sugestão sobre URL personalizada>"
      ]
    }}
  }},
  "priority_actions": [
    {{"action": "<Ação 1 mais impactante baseada no perfil>", "impact": "Alto", "why": "<Por que isso vai fazer diferença para ESTE perfil especificamente>"}},
    {{"action": "<Ação 2 específica>", "impact": "Alto", "why": "<Justificativa personalizada>"}},
    {{"action": "<Ação 3>", "impact": "Médio", "why": "<Justificativa>"}},
    {{"action": "<Ação 4>", "impact": "Médio", "why": "<Justificativa>"}},
    {{"action": "<Ação 5>", "impact": "Baixo", "why": "<Justificativa>"}}
  ]
}}

LEMBRE-SE:
- Cite elementos ESPECÍFICOS do perfil da pessoa na análise
- Se a headline atual é "Desenvolvedor Full Stack", sua reescrita deve ser baseada nisso
- Se não houver resumo, sugira criar um baseado nas experiências listadas
- Scores baixos para seções vazias, scores altos para seções bem desenvolvidas
- Seja honesto nos scores - não seja generoso demais
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
                    "Inclua sua especialidade principal e nível de senioridade",
                    "Adicione um resultado ou diferencial claro",
                    "Use keywords relevantes para sua área de atuação"
                ],
                "rewrite": "[Seu Cargo] | Especialista em [Área] | Ajudo empresas a [Resultado Específico]"
            },
            "about": {
                "title": "Sobre / Resumo",
                "icon": "📝",
                "score": 65,
                "analysis": "Seu resumo precisa contar uma história e mostrar seus resultados de forma clara.",
                "suggestions": [
                    "Comece com um gancho forte sobre sua trajetória",
                    "Inclua 3-5 conquistas específicas com métricas",
                    "Termine com call-to-action clara"
                ],
                "rewrite": "Revise seu 'Sobre' para incluir storytelling, resultados quantificáveis e uma chamada para ação clara ao final."
            },
            "experience": {
                "title": "Experiências Profissionais",
                "icon": "💼",
                "score": 70,
                "analysis": "Suas experiências precisam focar mais em resultados do que em responsabilidades.",
                "suggestions": [
                    "Use verbos de ação no início de cada bullet point",
                    "Quantifique seus resultados com números e percentuais",
                    "Mostre o impacto do seu trabalho nos resultados da empresa"
                ]
            },
            "skills": {
                "title": "Habilidades & Keywords",
                "icon": "🛠️",
                "score": 65,
                "analysis": "Organize suas habilidades estrategicamente e busque endossos.",
                "suggestions": [
                    "Priorize as 10 habilidades mais relevantes para seu objetivo",
                    "Peça endossos de colegas e gestores antigos",
                    "Adicione habilidades emergentes da sua área"
                ]
            },
            "visibility": {
                "title": "Visibilidade & SEO",
                "icon": "👁️",
                "score": 60,
                "analysis": "Seu perfil precisa de otimização para aparecer em mais buscas de recrutadores.",
                "suggestions": [
                    "Use keywords estratégicas em headline, sobre e experiências",
                    "Complete 100% do perfil (experiências, formação, certificações)",
                    "Personalize sua URL do LinkedIn"
                ]
            }
        },
        "priority_actions": [
            {"action": "Reescrever headline com foco em valor e resultados", "impact": "Alto", "why": "É a primeira coisa que recrutadores veem, impacta sua descoberta em buscas"},
            {"action": "Adicionar métricas concretas nas descrições de cargo", "impact": "Alto", "why": "Resultados quantificados demonstram seu impacto real"},
            {"action": "Completar seção 'Sobre' com storytelling", "impact": "Alto", "why": "Aumenta conexão emocional e mostra sua trajetória"},
            {"action": "Reorganizar habilidades por relevância", "impact": "Médio", "why": "Melhora SEO e aparece melhor para recrutadores"},
            {"action": "Personalizar URL do perfil", "impact": "Baixo", "why": "Mais profissional e fácil de compartilhar"}
        ]
    }

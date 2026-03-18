import json
import requests


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
    """Análise usando Groq API"""

    analysis_prompt = f"""
Você é um **especialista sênior em recrutamento, personal branding e otimização estratégica de perfis LinkedIn**.

Seu objetivo é realizar uma **análise profunda, estratégica e personalizada** do perfil abaixo.

A análise deve ir além de dicas superficiais: avalie **posicionamento profissional, clareza de valor, senioridade percebida, uso de keywords, storytelling e impacto profissional**.

PERFIL LINKEDIN (extraído de PDF):

{pdf_text[:15000]}

DIRETRIZES DE ANÁLISE:

1. Analise o **conteúdo real** do perfil.
2. Cite **elementos específicos do perfil sempre que possível**.
3. Seja **honesto e analítico**, não excessivamente generoso nas pontuações.
4. Identifique **pontos fortes claros** do perfil.
5. Identifique **oportunidades reais de melhoria**.
6. Avalie o **posicionamento profissional da pessoa no mercado**.
7. Avalie se o perfil comunica claramente:
   - especialidade
   - senioridade
   - impacto profissional
   - diferenciação no mercado.
8. Sugestões devem ser **específicas, acionáveis e estratégicas**.
9. As reescritas devem **manter a identidade profissional da pessoa**, apenas tornando o texto mais forte e claro.
10. Seja **profissional, respeitoso e construtivo**.
11. Você pode ser **analítico e crítico**, mas sempre com empatia.

IMPORTANTE:

Cada dimensão deve conter **EXATAMENTE 3 sugestões**.

As sugestões devem:

- ser específicas
- ser aplicáveis
- melhorar a percepção do perfil

Se alguma seção estiver **ausente ou fraca**, explique claramente.

Se o perfil estiver em outro idioma, traduza sua análise para português.

Retorne **APENAS JSON VÁLIDO**, sem markdown, sem explicações.

Estrutura obrigatória:

{{
  "overall_score": <0-100>,
  "dimensions": {{
    "headline": {{
      "title": "Headline & Primeira Impressão",
      "icon": "🎯",
      "score": <0-100>,
      "analysis": "<análise estratégica da headline atual: clareza de valor, keywords, impacto, diferenciação>",
      "suggestions": [
        "<sugestão específica baseada no conteúdo atual>",
        "<sugestão estratégica para melhorar posicionamento>",
        "<sugestão prática para aumentar impacto>"
      ],
      "rewrite": "<versão otimizada da headline mantendo a área e experiência da pessoa>"
    }},
    "about": {{
      "title": "Sobre / Resumo",
      "icon": "📝",
      "score": <0-100>,
      "analysis": "<análise da narrativa profissional: clareza, storytelling, autoridade, resultados>",
      "suggestions": [
        "<sugestão de melhoria narrativa>",
        "<sugestão para incluir conquistas ou métricas>",
        "<sugestão para melhorar posicionamento profissional>"
      ],
      "rewrite": "<versão otimizada do resumo mantendo a essência da história profissional>"
    }},
    "experience": {{
      "title": "Experiências Profissionais",
      "icon": "💼",
      "score": <0-100>,
      "analysis": "<análise das experiências: clareza, foco em impacto, senioridade percebida>",
      "suggestions": [
        "<sugestão para melhorar descrição de impacto>",
        "<sugestão para incluir resultados ou métricas>",
        "<sugestão para melhorar narrativa de carreira>"
      ]
    }},
    "skills": {{
      "title": "Habilidades & Keywords",
      "icon": "🛠️",
      "score": <0-100>,
      "analysis": "<análise da estratégia de habilidades e keywords>",
      "suggestions": [
        "<sugestão de habilidades estratégicas>",
        "<sugestão de reorganização>",
        "<sugestão de keywords relevantes>"
      ]
    }},
    "visibility": {{
      "title": "Visibilidade & SEO",
      "icon": "👁️",
      "score": <0-100>,
      "analysis": "<análise da otimização para busca e completude do perfil>",
      "suggestions": [
        "<sugestão para melhorar descoberta por recrutadores>",
        "<sugestão sobre seções faltantes>",
        "<sugestão sobre otimização de perfil>"
      ]
    }}
  }},
  "priority_actions": [
    {{"action": "<ação mais impactante>", "impact": "Alto", "why": "<justificativa estratégica baseada no perfil>"}},
    {{"action": "<segunda ação>", "impact": "Alto", "why": "<justificativa>"}},
    {{"action": "<terceira ação>", "impact": "Médio", "why": "<justificativa>"}},
    {{"action": "<quarta ação>", "impact": "Médio", "why": "<justificativa>"}},
    {{"action": "<quinta ação>", "impact": "Baixo", "why": "<justificativa>"}}
  ]
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em recrutamento e otimização de perfis LinkedIn. Retorne sempre JSON válido."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 4500
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
        content = result["choices"][0]["message"]["content"]

        # limpeza de markdown se existir
        content = content.strip()

        if content.startswith("```json"):
            content = content[7:]

        if content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        analysis_result = json.loads(content)

        if progress_callback:
            progress_callback(1.0)

        return analysis_result

    except json.JSONDecodeError:
        return create_fallback_analysis(pdf_text)

    except Exception as e:
        raise Exception(f"Erro ao chamar Groq API: {str(e)}")


def create_fallback_analysis(pdf_text):
    """Fallback caso a IA falhe"""

    return {
        "overall_score": 65,
        "dimensions": {
            "headline": {
                "title": "Headline & Primeira Impressão",
                "icon": "🎯",
                "score": 60,
                "analysis": "Sua headline poderia comunicar melhor sua especialidade e proposta de valor.",
                "suggestions": [
                    "Inclua sua especialidade principal e senioridade",
                    "Adicione uma proposta de valor clara",
                    "Inclua keywords estratégicas da sua área"
                ],
                "rewrite": "[Seu Cargo] | Especialista em [Área] | Gerando impacto através de [Competência-chave]"
            },
            "about": {
                "title": "Sobre / Resumo",
                "icon": "📝",
                "score": 65,
                "analysis": "Seu resumo poderia contar melhor sua trajetória profissional e destacar resultados concretos.",
                "suggestions": [
                    "Comece com um posicionamento profissional claro",
                    "Inclua conquistas mensuráveis",
                    "Finalize com call-to-action"
                ],
                "rewrite": "Profissional especializado em [área], com experiência em transformar dados e processos em decisões estratégicas."
            },
            "experience": {
                "title": "Experiências Profissionais",
                "icon": "💼",
                "score": 70,
                "analysis": "Suas experiências poderiam enfatizar mais impacto e resultados.",
                "suggestions": [
                    "Use verbos de ação no início das descrições",
                    "Adicione métricas de impacto",
                    "Destaque projetos relevantes"
                ]
            },
            "skills": {
                "title": "Habilidades & Keywords",
                "icon": "🛠️",
                "score": 65,
                "analysis": "Organizar habilidades estrategicamente pode melhorar sua descoberta por recrutadores.",
                "suggestions": [
                    "Priorize habilidades estratégicas",
                    "Adicione competências emergentes",
                    "Busque endossos relevantes"
                ]
            },
            "visibility": {
                "title": "Visibilidade & SEO",
                "icon": "👁️",
                "score": 60,
                "analysis": "Seu perfil pode ser melhor otimizado para buscas no LinkedIn.",
                "suggestions": [
                    "Use keywords estratégicas nas seções principais",
                    "Complete todas as seções do perfil",
                    "Personalize sua URL do LinkedIn"
                ]
            }
        },
        "priority_actions": [
            {"action": "Melhorar headline com posicionamento claro", "impact": "Alto", "why": "Impacta diretamente a primeira impressão e busca"},
            {"action": "Adicionar métricas de impacto nas experiências", "impact": "Alto", "why": "Resultados quantificados aumentam credibilidade"},
            {"action": "Reescrever resumo com storytelling profissional", "impact": "Alto", "why": "Melhora conexão e narrativa de carreira"},
            {"action": "Otimizar habilidades estratégicas", "impact": "Médio", "why": "Melhora SEO no LinkedIn"},
            {"action": "Completar otimizações de perfil", "impact": "Baixo", "why": "Aumenta profissionalismo geral"}
        ]
    }
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
    """Análise detalhada usando Groq API (Llama 3.3 70B)"""
    
    # Prompt otimizado para análises descritivas e personalizadas
    analysis_prompt = f"""Você é um especialista sênior em otimização de perfis LinkedIn e recrutamento executivo. Analise o perfil abaixo de forma PROFUNDA e PERSONALIZADA.

PERFIL LINKEDIN:
{pdf_text[:8000]}

INSTRUÇÕES CRÍTICAS:
1. Analise o CONTEÚDO REAL E ESPECÍFICO do perfil acima
2. Cite exemplos EXATOS do que a pessoa escreveu
3. Seja DESCRITIVO e DETALHADO - não economize nas palavras
4. Para cada dimensão, escreva análises de 4-6 parágrafos completos
5. Explique COMO fazer cada melhoria no LinkedIn (passos práticos)
6. Identifique pontos fortes específicos E áreas de melhoria
7. Use formatação HTML para destacar informações importantes

Retorne APENAS um JSON válido (sem markdown, sem ```json) com esta estrutura:

{{
  "overall_score": <número de 0-100 baseado na análise real>,
  "dimensions": {{
    "headline": {{
      "title": "Headline & Primeira Impressão",
      "icon": "🎯",
      "score": <0-100>,
      "detailed_analysis": "<p>Análise completa em HTML com 4-6 parágrafos. Cite a headline atual da pessoa entre aspas. Explique o que funciona e o que não funciona. Dê exemplos concretos de melhorias. Use <strong> para destacar pontos importantes. Inclua uma seção 'Como Melhorar no LinkedIn:' com passos práticos numerados.</p><p>Segundo parágrafo com mais detalhes...</p><p>Terceiro parágrafo...</p>"
    }},
    "about": {{
      "title": "Sobre / Resumo",
      "icon": "📝",
      "score": <0-100>,
      "detailed_analysis": "<p>Análise profunda do resumo atual. Cite trechos específicos. Se não houver resumo, explique o impacto negativo. Proponha estrutura ideal: gancho inicial, trajetória, conquistas com métricas, diferenciais, call-to-action.</p><p>Como editar: vá em 'Adicionar seção de perfil' → 'Resumo'...</p>"
    }},
    "experience": {{
      "title": "Experiências Profissionais",
      "icon": "💼",
      "score": <0-100>,
      "detailed_analysis": "<p>Análise detalhada de como as experiências estão descritas. Cite exemplos de cargos específicos da pessoa. Avalie uso de verbos de ação, presença de métricas, clareza de resultados. Compare com melhores práticas.</p><p>Passo a passo para melhorar: clique no cargo → 'Editar' → reescreva começando com verbo de ação...</p>"
    }},
    "skills": {{
      "title": "Habilidades & Otimização",
      "icon": "🛠️",
      "score": <0-100>,
      "detailed_analysis": "<p>Avaliação das habilidades listadas (ou ausentes). Priorização estratégica. Análise de relevância para a área. Estratégia de endossos.</p><p>Como otimizar: vá em 'Habilidades' → 'Adicionar habilidade' → priorize as top 10...</p>"
    }},
    "visibility": {{
      "title": "Visibilidade & Alcance",
      "icon": "👁️",
      "score": <0-100>,
      "detailed_analysis": "<p>Análise de otimização SEO, completude do perfil, URL personalizada, modo de abertura para oportunidades. Impacto na descoberta por recrutadores.</p><p>Checklist de otimização: 1. Personalize URL em 'Editar perfil público' 2. Ative 'Disponível para' 3. Complete todas seções...</p>"
    }}
  }},
  "priority_actions": [
    {{
      "action": "<Ação 1 mais impactante>",
      "impact": "Alto",
      "how_to": "<p>Explicação detalhada em HTML de COMO fazer essa ação no LinkedIn. Passo 1: clique em... Passo 2: navegue até... Passo 3: escreva seguindo este template... Inclua exemplos práticos e dicas específicas.</p><p>Por que isso é tão importante: explique o impacto nos resultados da pessoa.</p>"
    }},
    {{
      "action": "<Ação 2>",
      "impact": "Alto",
      "how_to": "<p>Passo a passo detalhado...</p>"
    }},
    {{
      "action": "<Ação 3>",
      "impact": "Médio",
      "how_to": "<p>Instruções práticas...</p>"
    }},
    {{
      "action": "<Ação 4>",
      "impact": "Médio",
      "how_to": "<p>Como executar...</p>"
    }},
    {{
      "action": "<Ação 5>",
      "impact": "Baixo",
      "how_to": "<p>Orientações...</p>"
    }}
  ]
}}

REGRAS DE OURO:
- SEMPRE cite conteúdo específico do perfil analisado
- SEMPRE explique como fazer as melhorias passo-a-passo
- Use HTML para formatação (<p>, <strong>, <em>, listas <ul><li>)
- Seja honesto nos scores - não infle artificialmente
- Mínimo de 300 palavras por dimensão
- Máximo de 600 palavras por dimensão
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
                "content": "Você é um especialista sênior em LinkedIn e recrutamento executivo. Retorne sempre JSON válido com análises detalhadas em HTML."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 8000
    }
    
    if progress_callback:
        progress_callback(0.3)
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=90
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

def create_fallback_analysis(pdf_text):
    """Cria uma análise básica de fallback caso a IA falhe"""
    
    return {
        "overall_score": 65,
        "dimensions": {
            "headline": {
                "title": "Headline & Primeira Impressão",
                "icon": "🎯",
                "score": 60,
                "detailed_analysis": """
                <p><strong>Análise da Headline:</strong> Sua headline atual precisa ser mais específica e mostrar seu valor único de forma clara. Uma headline genérica como apenas o cargo não destaca você em meio aos milhares de profissionais da mesma área no LinkedIn.</p>
                
                <p>Uma headline eficaz deve comunicar três elementos essenciais: <strong>quem você é</strong>, <strong>o que você faz</strong> e <strong>qual valor você entrega</strong>. A fórmula ideal é: [Cargo/Especialidade] | [Área de Expertise] | [Resultado que Entrega].</p>
                
                <p><strong>Como Melhorar no LinkedIn:</strong></p>
                <p>1. Clique no ícone de lápis ao lado da sua foto de perfil<br>
                2. No campo "Título", reescreva usando a fórmula acima<br>
                3. Inclua 2-3 keywords que recrutadores buscam na sua área<br>
                4. Mantenha entre 120-220 caracteres para não ser cortado</p>
                
                <p><strong>Exemplo prático:</strong> Em vez de "Desenvolvedor Full Stack", use "Senior Full Stack Developer | React & Node.js | Construindo produtos digitais escaláveis para startups e scale-ups"</p>
                """
            },
            "about": {
                "title": "Sobre / Resumo",
                "icon": "📝",
                "score": 65,
                "detailed_analysis": """
                <p><strong>Análise do Resumo:</strong> Seu resumo precisa contar uma história convincente e mostrar seus resultados de forma clara e quantificável. É sua chance de se conectar emocionalmente com recrutadores e mostrar por que você é único.</p>
                
                <p>Um resumo eficaz segue esta estrutura: <strong>Gancho inicial</strong> (frase impactante), <strong>Trajetória</strong> (sua jornada em 2-3 frases), <strong>Expertise e Conquistas</strong> (com números), <strong>Diferenciais</strong> (o que te torna único), e <strong>Call-to-Action</strong> (como te contatar).</p>
                
                <p><strong>Como Editar no LinkedIn:</strong></p>
                <p>1. Vá até a seção "Sobre" no seu perfil<br>
                2. Clique no ícone de lápis para editar<br>
                3. Reescreva seguindo a estrutura acima<br>
                4. Use parágrafos curtos (2-3 linhas) para facilitar leitura<br>
                5. Inclua emojis estrategicamente para destacar pontos chave</p>
                
                <p><strong>Dica Pro:</strong> Use a primeira pessoa ("Eu ajudo...") para criar conexão pessoal. Inclua 3-5 resultados específicos com métricas (ex: "aumentei vendas em 40%", "gerenciei equipe de 15 pessoas").</p>
                """
            },
            "experience": {
                "title": "Experiências Profissionais",
                "icon": "💼",
                "score": 70,
                "detailed_analysis": """
                <p><strong>Análise das Experiências:</strong> Suas descrições de cargo precisam focar mais em <strong>resultados e impacto</strong> do que em responsabilidades. Recrutadores querem saber o que você conquistou, não apenas o que você fazia no dia a dia.</p>
                
                <p>A fórmula ideal para cada experiência: <strong>Verbo de Ação + O que fez + Como fez + Resultado Quantificado</strong>. Por exemplo: "Implementei metodologia ágil (Scrum) que reduziu tempo de desenvolvimento em 30% e aumentou satisfação do cliente de 3.2 para 4.8 estrelas".</p>
                
                <p><strong>Como Melhorar no LinkedIn:</strong></p>
                <p>1. Clique no ícone de lápis em cada cargo<br>
                2. Reescreva cada bullet point começando com verbo de ação forte (Liderou, Implementou, Otimizou, Desenvolveu)<br>
                3. Adicione números e percentuais específicos de resultados<br>
                4. Use 4-6 bullet points por cargo (não mais)<br>
                5. Foque nos últimos 10 anos - cargos antigos podem ser resumidos</p>
                
                <p><strong>Lista de Verbos Poderosos:</strong> Liderou, Impulsionou, Aumentou, Reduziu, Implementou, Otimizou, Gerenciou, Desenvolveu, Transformou, Conquistou.</p>
                """
            },
            "skills": {
                "title": "Habilidades & Otimização",
                "icon": "🛠️",
                "score": 65,
                "detailed_analysis": """
                <p><strong>Análise de Habilidades:</strong> A organização estratégica das suas habilidades é crucial para SEO do LinkedIn e para aparecer em buscas de recrutadores. As primeiras 3 habilidades são as mais importantes e devem refletir sua expertise principal.</p>
                
                <p>Você deve ter entre 15-50 habilidades listadas, priorizando as mais relevantes para seu objetivo profissional atual. Habilidades com mais endossos aparecem melhor nas buscas.</p>
                
                <p><strong>Como Otimizar no LinkedIn:</strong></p>
                <p>1. Vá até a seção "Habilidades"<br>
                2. Clique em "Adicionar habilidade" e adicione as top 10 da sua área<br>
                3. Reordene arrastando as 3 mais importantes para o topo<br>
                4. Peça endossos: envie mensagem para 10-15 colegas pedindo endosso específico<br>
                5. Retribua endossando habilidades deles também</p>
                
                <p><strong>Estratégia de Endossos:</strong> Priorize pedir endossos de gestores e clientes. Mensagem sugerida: "Oi [Nome], estamos trabalhando juntos em [Projeto] e gostaria de saber se você poderia endossar minha habilidade em [Skill]. Posso retribuir endossando suas habilidades também!"</p>
                """
            },
            "visibility": {
                "title": "Visibilidade & Alcance",
                "icon": "👁️",
                "score": 60,
                "detailed_analysis": """
                <p><strong>Análise de Visibilidade:</strong> Seu perfil precisa estar otimizado para SEO do LinkedIn para aparecer em buscas de recrutadores. Isso inclui URL personalizada, modo "Disponível para oportunidades", e completude de 100% do perfil.</p>
                
                <p>Perfis completos aparecem 40x mais em buscas do LinkedIn. Keywords estratégicas em headline, resumo e experiências aumentam drasticamente suas chances de ser encontrado.</p>
                
                <p><strong>Checklist de Otimização (Faça Agora):</strong></p>
                <p>1. <strong>URL Personalizada:</strong> Vá em "Editar perfil público" → "Editar URL" → use linkedin.com/in/seunome<br>
                2. <strong>Disponível para Oportunidades:</strong> Clique em "Disponível para" → Ative "Fornecendo serviços" ou "Contratação"<br>
                3. <strong>Foto Profissional:</strong> Use foto com fundo neutro, você sorrindo, e resolução mínima 400x400px<br>
                4. <strong>Banner Personalizado:</strong> Crie um banner 1584x396px com sua área de atuação<br>
                5. <strong>Complete 100%:</strong> Adicione formação, certificações, projetos, idiomas</p>
                
                <p><strong>Dica SEO:</strong> Use as 5 keywords mais buscadas da sua área no resumo (repita 2-3x de forma natural).</p>
                """
            }
        },
        "priority_actions": [
            {
                "action": "Reescrever headline com fórmula [Cargo] | [Expertise] | [Valor]",
                "impact": "Alto",
                "how_to": """
                <p><strong>Passo a Passo Detalhado:</strong></p>
                <p>1. <strong>Pesquise perfis top:</strong> Busque no LinkedIn 3-5 profissionais seniores da sua área e veja como escreveram suas headlines<br>
                2. <strong>Identifique suas keywords:</strong> Quais termos recrutadores buscam? (ex: Python, React, Scrum Master, etc)<br>
                3. <strong>Clique no lápis:</strong> Vá no seu perfil e clique no ícone de edição ao lado da foto<br>
                4. <strong>Escreva usando a fórmula:</strong> [Seu Cargo Sênior] | [2-3 Tecnologias/Skills Principais] | [Resultado que Entrega]<br>
                5. <strong>Exemplo real:</strong> "Senior Product Manager | SaaS B2B | Transformando dados em produtos que aumentam ROI em 3x"</p>
                
                <p><strong>Por que isso é crucial:</strong> Sua headline é a primeira (e às vezes única) coisa que recrutadores veem. Uma headline otimizada pode aumentar em 300% suas chances de ser encontrado em buscas.</p>
                """
            },
            {
                "action": "Adicionar 3-5 conquistas quantificadas em cada cargo",
                "impact": "Alto",
                "how_to": """
                <p><strong>Como Fazer:</strong></p>
                <p>1. Para cada cargo, liste suas 3-5 maiores conquistas<br>
                2. Para cada conquista, identifique o número/métrica: percentual de melhoria, valor economizado, pessoas gerenciadas, projetos entregues<br>
                3. Clique no lápis de cada cargo → Editar descrição<br>
                4. Reescreva usando: [Verbo de Ação] + [O que fez] + [Resultado com número]<br>
                5. Salve e repita para todos os cargos relevantes</p>
                
                <p><strong>Exemplos práticos:</strong> "Liderou equipe de 8 desenvolvedores na criação de plataforma que processou R$ 2M em transações no primeiro ano" | "Reduziu bugs em produção em 60% implementando testes automatizados com Jest e Cypress"</p>
                """
            },
            {
                "action": "Completar resumo 'Sobre' com estrutura storytelling",
                "impact": "Alto",
                "how_to": """
                <p><strong>Template de Resumo Campeão:</strong></p>
                <p><strong>Parágrafo 1 - Gancho:</strong> Comece com uma frase impactante sobre sua paixão ou resultado mais impressionante<br>
                <strong>Parágrafo 2 - Trajetória:</strong> Resuma sua jornada profissional em 2-3 frases<br>
                <strong>Parágrafo 3 - Expertise:</strong> Liste 3-5 suas principais habilidades/conquistas com números<br>
                <strong>Parágrafo 4 - Diferencial:</strong> O que te torna único? Sua abordagem, valores, especialização<br>
                <strong>Parágrafo 5 - CTA:</strong> Como as pessoas podem te contatar e para quê</p>
                
                <p><strong>Onde editar:</strong> Seção "Sobre" → Ícone de lápis → Cole seu novo resumo → Salvar</p>
                """
            },
            {
                "action": "Personalizar URL e ativar 'Disponível para oportunidades'",
                "impact": "Médio",
                "how_to": """
                <p><strong>URL Personalizada:</strong> Perfil → "Editar perfil público" → "Editar URL" → Digite: linkedin.com/in/seunome-sobrenome → Salvar</p>
                
                <p><strong>Disponível para Oportunidades:</strong> Ícone "Disponível para" (abaixo da foto) → Marque "Contratação" ou "Fornecendo serviços" → Escolha o que você busca → Salvar</p>
                
                <p><strong>Impacto:</strong> Isso sinaliza para recrutadores que você está aberto a oportunidades SEM alertar sua empresa atual (é privado).</p>
                """
            },
            {
                "action": "Adicionar foto profissional e banner personalizado",
                "impact": "Baixo",
                "how_to": """
                <p><strong>Foto:</strong> Use foto profissional (não selfie), fundo neutro, você sorrindo, roupas adequadas à sua área. Resolução mínima 400x400px.</p>
                
                <p><strong>Banner:</strong> Crie um banner 1584x396px no Canva com: seu nome, área de atuação, e um visual profissional relacionado ao seu trabalho.</p>
                
                <p><strong>Upload:</strong> Clique na câmera sobre a foto/banner → Upload → Ajuste enquadramento → Aplicar</p>
                """
            }
        ]
    }

import streamlit as st
import os
from datetime import datetime
from utils.pdf_parser import extract_text_from_pdf
from utils.linkedin_analyzer import analyze_profile
from utils.sheets_handler import save_lead_to_sheets

# Configuração da página
st.set_page_config(
    page_title="LinkedPro Analyzer - Análise Gratuita de Perfil LinkedIn",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para design editorial/profissional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Work+Sans:wght@400;500;600&display=swap');
    
    /* Reset e Base */
    .main {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
        color: #e8e8e8;
    }
    
    /* Tipografia Distintiva */
    h1, h2, h3 {
        font-family: 'Crimson Pro', serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    p, div, span, label {
        font-family: 'Work Sans', sans-serif !important;
    }
    
    /* Header Principal */
    .hero-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(120deg, #ff6b35 0%, #f7931e 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(255, 107, 53, 0.3);
    }
    
    .hero-header h1 {
        font-size: 3.5rem;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-header p {
        font-size: 1.3rem;
        color: #fff5e1;
        font-weight: 400;
    }
    
    /* Cards */
    .stCard {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 107, 53, 0.3);
        border-radius: 12px;
        color: #ffffff;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b35;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
        background: rgba(255, 255, 255, 0.12);
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(120deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(255, 107, 53, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(255, 107, 53, 0.4);
    }
    
    /* Score Badges */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 0.5rem;
    }
    
    .score-excellent {
        background: linear-gradient(120deg, #00d4aa 0%, #00b894 100%);
        color: white;
    }
    
    .score-good {
        background: linear-gradient(120deg, #ffd93d 0%, #f39c12 100%);
        color: #1a1a2e;
    }
    
    .score-needs-work {
        background: linear-gradient(120deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(120deg, #ff6b35 0%, #f7931e 100%);
        border-radius: 10px;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 107, 53, 0.5);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 107, 53, 0.1);
        border-radius: 12px;
        font-weight: 600;
        color: #ff6b35;
    }
    
    /* Stats */
    .stat-box {
        background: rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #ff6b35;
        margin: 1rem 0;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ff6b35;
        font-family: 'Crimson Pro', serif;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #b8b8b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero-header">
    <h1>🚀 LinkedPro Analyzer</h1>
    <p>Análise profissional GRATUITA do seu perfil LinkedIn com IA</p>
</div>
""", unsafe_allow_html=True)

# Inicializar session state
if 'lead_captured' not in st.session_state:
    st.session_state.lead_captured = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# ETAPA 1: Captura de Lead
if not st.session_state.lead_captured:
    st.markdown("### 📝 Primeiro, vamos nos conhecer")
    st.markdown("*Seus dados são seguros e usados apenas para enviar sua análise*")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Seu nome completo", placeholder="João Silva")
    with col2:
        email = st.text_input("Seu melhor e-mail", placeholder="joao@email.com")
    
    if st.button("Continuar para Análise →"):
        if name and email and "@" in email:
            # Salvar lead
            try:
                save_lead_to_sheets(name, email)
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.lead_captured = True
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar lead: {str(e)}")
                st.info("Continuando mesmo assim...")
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.lead_captured = True
                st.rerun()
        else:
            st.error("Por favor, preencha nome e e-mail válidos!")

# ETAPA 2: Upload e Análise
else:
    st.markdown(f"### Olá, {st.session_state.user_name}! 👋")
    
    # Instruções para baixar PDF
    with st.expander("📥 Como baixar o PDF do seu perfil LinkedIn?", expanded=True):
        st.markdown("""
        **Passo a passo simples:**
        
        1. Acesse seu perfil no LinkedIn (linkedin.com/in/seu-perfil)
        2. Clique em **"Mais"** (abaixo da sua foto)
        3. Selecione **"Salvar como PDF"**
        4. Faça o download do arquivo
        5. Faça upload aqui abaixo! 🎯
        
        *O processo leva menos de 1 minuto!*
        """)
    
    # Upload do PDF
    uploaded_file = st.file_uploader(
        "📄 Faça upload do PDF do seu perfil LinkedIn",
        type=['pdf'],
        help="Aceita apenas arquivos PDF baixados do LinkedIn"
    )
    
    # Configuração da API
    st.markdown("### 🔑 Configuração da IA")
    
    api_choice = st.radio(
        "Escolha a API de IA:",
        ["Groq (Recomendado - Grátis)", "OpenAI GPT-4"],
        help="Groq é gratuito e super rápido!"
    )
    
    if api_choice == "Groq (Recomendado - Grátis)":
        with st.expander("🆓 Como conseguir sua API Key Groq (100% Grátis)"):
            st.markdown("""
            1. Acesse: [https://console.groq.com](https://console.groq.com)
            2. Faça login/cadastro (Gmail funciona)
            3. Vá em **API Keys** → **Create API Key**
            4. Copie a chave e cole abaixo
            
            *Não precisa cartão de crédito! É 100% gratuito.*
            """)
        api_key = st.text_input("Sua Groq API Key:", type="password", placeholder="gsk_...")
    else:
        api_key = st.text_input("Sua OpenAI API Key:", type="password", placeholder="sk-...")
    
    # Botão de análise
    if uploaded_file and api_key:
        if st.button("🚀 Analisar Meu Perfil Agora!", key="analyze_btn"):
            with st.spinner("🔍 Analisando seu perfil... Isso pode levar 30-60 segundos..."):
                try:
                    # Extrair texto do PDF
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if len(pdf_text) < 100:
                        st.error("O PDF parece estar vazio ou corrompido. Tente baixar novamente do LinkedIn.")
                    else:
                        # Analisar com IA
                        progress_bar = st.progress(0)
                        
                        analysis_result = analyze_profile(
                            pdf_text, 
                            api_key, 
                            api_choice,
                            progress_callback=progress_bar.progress
                        )
                        
                        st.session_state.analysis_result = analysis_result
                        st.session_state.analysis_complete = True
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Erro na análise: {str(e)}")
                    st.info("Verifique se sua API Key está correta e tente novamente.")
    
    # Mostrar resultado
    if st.session_state.analysis_complete and 'analysis_result' in st.session_state:
        result = st.session_state.analysis_result
        
        st.markdown("---")
        st.markdown("## 📊 Sua Análise Completa")
        
        # Score Geral
        overall_score = result.get('overall_score', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{overall_score}/100</div>
                <div class="stat-label">Score Geral</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            improvement_potential = 100 - overall_score
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">+{improvement_potential}%</div>
                <div class="stat-label">Potencial de Melhoria</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            priority_items = len(result.get('priority_actions', []))
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{priority_items}</div>
                <div class="stat-label">Ações Prioritárias</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análises por dimensão
        st.markdown("### 🎯 Análise Detalhada por Dimensão")
        
        dimensions = result.get('dimensions', {})
        
        for dim_name, dim_data in dimensions.items():
            with st.expander(f"**{dim_data['icon']} {dim_data['title']}** - Score: {dim_data['score']}/100", expanded=True):
                # Badge de score
                score = dim_data['score']
                if score >= 80:
                    badge_class = "score-excellent"
                    status = "Excelente! ✨"
                elif score >= 60:
                    badge_class = "score-good"
                    status = "Bom, mas pode melhorar 💪"
                else:
                    badge_class = "score-needs-work"
                    status = "Precisa de atenção 🎯"
                
                st.markdown(f'<span class="score-badge {badge_class}">{score}/100 - {status}</span>', unsafe_allow_html=True)
                
                # Análise
                st.markdown("**📝 Análise:**")
                st.markdown(dim_data['analysis'])
                
                # Sugestões
                if dim_data.get('suggestions'):
                    st.markdown("**💡 Sugestões de Melhoria:**")
                    for suggestion in dim_data['suggestions']:
                        st.markdown(f"- {suggestion}")
                
                # Reescrita (se disponível)
                if dim_data.get('rewrite'):
                    st.markdown("**✨ Versão Reescrita (pronta para copiar):**")
                    st.code(dim_data['rewrite'], language=None)
        
        # Checklist Priorizado
        st.markdown("### ✅ Checklist de Ações Prioritárias")
        st.markdown("*Faça nesta ordem para máximo impacto:*")
        
        for i, action in enumerate(result.get('priority_actions', []), 1):
            st.markdown(f"{i}. **{action['action']}** - Impacto: {action['impact']}")
            st.markdown(f"   *{action['why']}*")
        
        # Download do resultado
        st.markdown("### 📥 Salvar Análise")
        
        # Criar markdown para download
        download_content = f"""# Análise LinkedPro - {st.session_state.user_name}
        
## Score Geral: {overall_score}/100

## Análises Detalhadas

"""
        for dim_name, dim_data in dimensions.items():
            download_content += f"\n### {dim_data['title']} ({dim_data['score']}/100)\n\n"
            download_content += f"{dim_data['analysis']}\n\n"
            if dim_data.get('suggestions'):
                download_content += "**Sugestões:**\n"
                for suggestion in dim_data['suggestions']:
                    download_content += f"- {suggestion}\n"
            download_content += "\n"
        
        download_content += "\n## Checklist Prioritário\n\n"
        for i, action in enumerate(result.get('priority_actions', []), 1):
            download_content += f"{i}. {action['action']} (Impacto: {action['impact']})\n"
        
        st.download_button(
            label="📄 Baixar Análise Completa (Markdown)",
            data=download_content,
            file_name=f"linkedin_analysis_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        
        # CTA Final
        st.markdown("---")
        st.markdown("""
        ### 🎉 Gostou da análise?
        
        Compartilhe com seus amigos que também querem melhorar seus perfis no LinkedIn!
        
        **LinkedPro Analyzer** - 100% Gratuito, sempre! 🚀
        """)
        
        if st.button("🔄 Analisar Outro Perfil"):
            st.session_state.analysis_complete = False
            st.session_state.analysis_result = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem;'>
    <p>Feito com ❤️ usando IA • 100% Gratuito • Seus dados são privados</p>
</div>
""", unsafe_allow_html=True)

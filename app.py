import streamlit as st
from datetime import datetime
from utils.pdf_parser import extract_text_from_pdf
from utils.linkedin_analyzer import analyze_profile

# API Key do Groq (configurada pelo admin)
GROQ_API_KEY = "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"

# Configuração da página
st.set_page_config(
    page_title="LinkedPro Analyzer - Análise Gratuita de Perfil LinkedIn",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado - Estilo ZenOffice
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset e Base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    /* Header Principal */
    .hero-header {
        text-align: center;
        padding: 2.5rem 2rem 2rem;
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-header h1 {
        font-size: 2.5rem;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .hero-header p {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.75rem;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
    }
    
    /* Score Badges */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .score-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .score-good {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .score-needs-work {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        border-radius: 10px;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(79, 70, 229, 0.4);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(79, 70, 229, 0.6);
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Stats */
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .stat-box:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6366f1;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.5rem;
    }
    
    /* Dimension Card */
    .dimension-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .dimension-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .dimension-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #6366f1;
    }
    
    .suggestion-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 0.875rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #6366f1;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Botão de Café Flutuante */
    .cafe-button {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 999;
    }
    
    .cafe-button a {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.875rem 1.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3);
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .cafe-button a:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(245, 158, 11, 0.4);
    }
    
    /* Link do Perfil */
    .profile-link {
        text-align: center;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .profile-link a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .profile-link a:hover {
        color: #818cf8;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #4f46e5;
        border-radius: 10px;
    }
    
    /* Expander sem setinha */
    details {
        border: none !important;
    }
    
    summary {
        list-style: none !important;
    }
    
    summary::-webkit-details-marker {
        display: none !important;
    }
    
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        font-weight: 600;
        color: #6366f1;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero-header">
    <h1>🚀 LinkedPro Analyzer</h1>
    <p>Análise Profissional Gratuita com IA</p>
</div>
""", unsafe_allow_html=True)

# Inicializar session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Upload e Análise
if not st.session_state.analysis_complete:
    st.markdown("### 📤 Faça upload do PDF do seu perfil LinkedIn")
    
    # Instruções para baixar PDF
    with st.expander("📥 Como baixar o PDF do seu perfil LinkedIn?", expanded=False):
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
        "📄 Selecione o PDF do seu perfil LinkedIn",
        type=['pdf'],
        help="Aceita apenas arquivos PDF baixados do LinkedIn"
    )
    
    # Botão de análise
    if uploaded_file:
        if st.button("🚀 Analisar Meu Perfil Agora!", key="analyze_btn", use_container_width=True):
            with st.spinner("🔍 Analisando seu perfil... Isso leva cerca de 10-15 segundos..."):
                try:
                    # Extrair texto do PDF
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if len(pdf_text) < 100:
                        st.error("O PDF parece estar vazio ou corrompido. Tente baixar novamente do LinkedIn.")
                    else:
                        # Analisar com IA usando Groq
                        progress_bar = st.progress(0)
                        
                        analysis_result = analyze_profile(
                            pdf_text, 
                            GROQ_API_KEY,
                            progress_callback=progress_bar.progress
                        )
                        
                        st.session_state.analysis_result = analysis_result
                        st.session_state.analysis_complete = True
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Erro na análise: {str(e)}")
                    st.info("Tente novamente em alguns segundos. Se o problema persistir, entre em contato.")

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
        # Card de dimensão
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
        
        st.markdown(f"""
        <div class="dimension-card">
            <div class="dimension-title">{dim_data['icon']} {dim_data['title']}</div>
            <span class="score-badge {badge_class}">{score}/100 - {status}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise
        st.markdown("**📝 Análise:**")
        st.markdown(dim_data['analysis'])
        
        # Sugestões em cards
        if dim_data.get('suggestions'):
            st.markdown("**💡 Ações Recomendadas:**")
            for suggestion in dim_data['suggestions']:
                st.markdown(f"""
                <div class="suggestion-item">
                    ✓ {suggestion}
                </div>
                """, unsafe_allow_html=True)
        
        # Reescrita (se disponível)
        if dim_data.get('rewrite'):
            st.markdown("**✨ Sugestão Personalizada:**")
            st.code(dim_data['rewrite'], language=None)
        
        st.markdown("")  # Espaço entre cards
    
    # Checklist Priorizado
    st.markdown("### ✅ Checklist de Ações Prioritárias")
    st.markdown("*Execute nesta ordem para máximo impacto:*")
    
    for i, action in enumerate(result.get('priority_actions', []), 1):
        st.markdown(f"""
        <div class="suggestion-item">
            <strong>{i}. {action['action']}</strong> - Impacto: {action['impact']}<br>
            <em>{action['why']}</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Download do resultado
    st.markdown("---")
    st.markdown("### 📥 Salvar Análise")
    
    # Criar markdown para download
    download_content = f"""# Análise LinkedPro
    
## Score Geral: {overall_score}/100

## Análises Detalhadas

"""
    for dim_name, dim_data in dimensions.items():
        download_content += f"\n### {dim_data['title']} ({dim_data['score']}/100)\n\n"
        download_content += f"{dim_data['analysis']}\n\n"
        if dim_data.get('suggestions'):
            download_content += "**Ações Recomendadas:**\n"
            for suggestion in dim_data['suggestions']:
                download_content += f"- {suggestion}\n"
        if dim_data.get('rewrite'):
            download_content += f"\n**Sugestão Personalizada:**\n{dim_data['rewrite']}\n"
        download_content += "\n"
    
    download_content += "\n## Checklist Prioritário\n\n"
    for i, action in enumerate(result.get('priority_actions', []), 1):
        download_content += f"{i}. {action['action']} (Impacto: {action['impact']})\n"
        download_content += f"   {action['why']}\n\n"
    
    st.download_button(
        label="📄 Baixar Análise Completa (Markdown)",
        data=download_content,
        file_name=f"linkedin_analysis_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    # CTA Final
    st.markdown("---")
    st.markdown("""
    ### 🎉 Gostou da análise?
    
    Compartilhe com seus amigos que também querem melhorar seus perfis no LinkedIn!
    
    **LinkedPro Analyzer** - 100% Gratuito, sempre! 🚀
    """)
    
    if st.button("🔄 Analisar Outro Perfil", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.analysis_result = None
        st.rerun()

# Botão de Café Flutuante (estilo ZenOffice)
st.markdown("""
<div class="cafe-button">
    <a href="https://buymeacoffee.com/marioschenkel" target="_blank">
        ☕ Pagar um Café
    </a>
</div>
""", unsafe_allow_html=True)

# Footer com link do perfil
st.markdown("---")
st.markdown("""
<div class="profile-link">
    <p style='color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;'>
        100% Gratuito • Seus dados são privados • Ao acessar você concorda com o uso de cookies • Desenvolvido por Mario Schenkel
    </p>
    <a href="https://linkedin.com/in/marioschenkel" target="_blank">
        👤 Desenvolvido por Mario Schenkel
    </a>
</div>
""", unsafe_allow_html=True)

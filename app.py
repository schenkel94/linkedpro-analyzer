import streamlit as st
from datetime import datetime
from utils.pdf_parser import extract_text_from_pdf
from utils.linkedin_analyzer import analyze_profile
import base64

# API Key do Groq (configurada pelo admin)
GROQ_API_KEY = "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"

# Configuração da página
st.set_page_config(
    page_title="LinkedPro Analyzer - Análise Gratuita de Perfil LinkedIn",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Função para carregar imagem como base64
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# CSS customizado - Estilo ZenOffice
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
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
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
    }
    
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .score-excellent { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }
    .score-good { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; }
    .score-needs-work { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; }
    
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        border-radius: 10px;
    }
    
    .stFileUploader {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(79, 70, 229, 0.4);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
        transition: all 0.2s ease;
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
    
    .dimension-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
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
    
    .projects-section {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .projects-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .project-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .project-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-4px);
    }
    
    .project-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #6366f1;
        margin: 1rem 0 0.5rem;
    }
    
    .project-description {
        font-size: 0.875rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background-color: #4f46e5; border-radius: 10px; }
    
    details { border: none !important; }
    summary { list-style: none !important; }
    summary::-webkit-details-marker { display: none !important; }
    
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
    
    with st.expander("📥 Como baixar o PDF do seu perfil LinkedIn?", expanded=False):
        st.markdown("""
        **Passo a passo simples:**
        
        1. Acesse seu perfil no LinkedIn (linkedin.com/in/seu-perfil)
        2. Clique em **"Mais"** (abaixo da sua foto)
        3. Selecione **"Salvar como PDF"**
        4. Faça o download do arquivo
        5. Faça upload aqui abaixo! 🎯
        """)
    
    uploaded_file = st.file_uploader(
        "📄 Selecione o PDF do seu perfil LinkedIn",
        type=['pdf'],
        help="Aceita apenas arquivos PDF baixados do LinkedIn"
    )
    
    if uploaded_file:
        if st.button("🚀 Analisar Meu Perfil Agora!", key="analyze_btn", use_container_width=True):
            with st.spinner("🔍 Analisando seu perfil..."):
                try:
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if len(pdf_text) < 100:
                        st.error("O PDF parece estar vazio. Tente baixar novamente.")
                    else:
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
                    st.error(f"❌ Erro: {str(e)}")

# Mostrar resultado
if st.session_state.analysis_complete and 'analysis_result' in st.session_state:
    result = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 Sua Análise Completa")
    
    overall_score = result.get('overall_score', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{overall_score}/100</div><div class="stat-label">Score Geral</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">+{100-overall_score}%</div><div class="stat-label">Potencial</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(result.get("priority_actions",[]))}</div><div class="stat-label">Ações</div></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Análise Detalhada")
    
    for dim_name, dim_data in result.get('dimensions', {}).items():
        score = dim_data['score']
        badge_class = "score-excellent" if score >= 80 else "score-good" if score >= 60 else "score-needs-work"
        status = "Excelente! ✨" if score >= 80 else "Bom 💪" if score >= 60 else "Atenção 🎯"
        
        st.markdown(f'<div class="dimension-card"><div class="dimension-title">{dim_data["icon"]} {dim_data["title"]}</div><span class="score-badge {badge_class}">{score}/100 - {status}</span></div>', unsafe_allow_html=True)
        st.markdown("**📝 Análise:**")
        st.markdown(dim_data['analysis'])
        
        if dim_data.get('suggestions'):
            st.markdown("**💡 Ações:**")
            for suggestion in dim_data['suggestions']:
                st.markdown(f'<div class="suggestion-item">✓ {suggestion}</div>', unsafe_allow_html=True)
        
        if dim_data.get('rewrite'):
            st.markdown("**✨ Sugestão:**")
            st.code(dim_data['rewrite'], language=None)
        st.markdown("")
    
    st.markdown("### ✅ Checklist Prioritário")
    for i, action in enumerate(result.get('priority_actions', []), 1):
        st.markdown(f'<div class="suggestion-item"><strong>{i}. {action["action"]}</strong> - {action["impact"]}<br><em>{action["why"]}</em></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    download_content = f"# Análise LinkedPro\n\n## Score: {overall_score}/100\n\n"
    st.download_button("📄 Baixar Análise", download_content, f"linkedin_analysis_{datetime.now().strftime('%Y%m%d')}.md", "text/markdown", use_container_width=True)
    
    if st.button("🔄 Analisar Outro Perfil", use_container_width=True):
        st.session_state.analysis_complete = False
        st.rerun()

# Seção Projetos
st.markdown('<div class="projects-section"><h2 class="projects-title">🚀 Outros Projetos</h2></div>', unsafe_allow_html=True)

# Tentar carregar capa do ZenOffice
zen_img = get_image_base64("capa_zenoffice.png")
img_html = f'<img src="data:image/png;base64,{zen_img}" style="width:100%;border-radius:12px;margin-bottom:1rem">' if zen_img else '<div style="width:100%;height:200px;background:rgba(99,102,241,0.2);border-radius:12px;margin-bottom:1rem;display:flex;align-items:center;justify-center;color:#6366f1;font-size:3rem;">⏱️</div>'

st.markdown(f"""
<a href="https://zenoffice.netlify.app" target="_blank" style="text-decoration:none">
    <div class="project-card">
        {img_html}
        <div class="project-name">ZenOffice</div>
        <div class="project-description">
            App de produtividade focado em bem-estar. Timer Pomodoro, tarefas, sons ambientes e respiração guiada.
        </div>
    </div>
</a>
""", unsafe_allow_html=True)

# Modal de Apoio
st.markdown("---")
with st.expander("☕ Apoiar o Desenvolvedor", expanded=False):
    tab1, tab2 = st.tabs(["💰 Apoiar", "👤 Sobre"])
    
    with tab1:
        qr_img = get_image_base64("qr.png")
        if qr_img:
            st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{qr_img}" style="max-width:240px;background:white;padding:1.5rem;border-radius:16px"></div>', unsafe_allow_html=True)
        
        pix_key = "df15a204-0a95-45da-8df5-c63ae7e9022e"
        st.code(pix_key, language=None)
        if st.button("📋 Copiar Chave PIX", use_container_width=True):
            st.success("✅ Chave copiada!")
    
    with tab2:
        profile_img = get_image_base64("profile.png")
        if profile_img:
            st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{profile_img}" style="width:120px;height:120px;border-radius:50%;border:3px solid rgba(99,102,241,0.3)"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem">
            <h3 style="color:#6366f1">Mário Schenkel</h3>
            <p style="color:#94a3b8;font-size:0.875rem">Criador do ZenOffice</p>
            <p style="color:#cbd5e1;font-size:0.875rem;line-height:1.6">Focado em criar soluções que trazem paz e produtividade.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="text-align:center;margin-top:1rem"><a href="https://linkedin.com/in/marioschenkel" target="_blank" style="background:linear-gradient(135deg,#4f46e5,#6366f1);color:white;padding:0.75rem 2rem;border-radius:12px;text-decoration:none;display:inline-block;font-weight:600">LinkedIn</a></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.875rem;padding:2rem 0;margin-top:2rem;border-top:1px solid rgba(255,255,255,0.1)">
    <p>Feito com ❤️ usando IA • 100% Gratuito • Seus dados são privados</p>
</div>
""", unsafe_allow_html=True)

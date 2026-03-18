import streamlit as st
import streamlit.components.v1 as components
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

# Inicializar session state para cookies
if 'cookies_accepted' not in st.session_state:
    # Verificar se já aceitou antes (usando query params como fallback)
    st.session_state.cookies_accepted = False

# Função para carregar imagem como base64
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# Carregar imagens
profile_img = get_image_base64("profile.png")
qr_img = get_image_base64("qr.png")
zen_icon = get_image_base64("icon_zenoffice.png")

# CSS + Botão Flutuante FIXO
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
        padding-bottom: 100px;
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
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
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
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .dimension-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #6366f1;
    }
    
    .dimension-content {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .dimension-content p {
        margin-bottom: 1rem;
    }
    
    .dimension-content strong {
        color: #e2e8f0;
        font-weight: 600;
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
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .project-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
    }
    
    .project-icon {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        flex-shrink: 0;
    }
    
    .project-info {
        flex: 1;
    }
    
    .project-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.5rem;
    }
    
    .project-description {
        font-size: 0.875rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Cookie Notice */
    .cookie-notice {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        z-index: 9998;
        animation: slideUpNotice 0.4s ease-out;
    }
    
    @keyframes slideUpNotice {
        from { transform: translateY(100%); }
        to { transform: translateY(0); }
    }
    
    .cookie-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .cookie-text {
        color: #cbd5e1;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    .cookie-btn {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    
    .cookie-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
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
            with st.spinner("🔍 Analisando seu perfil com profundidade... Isso pode levar 20-30 segundos."):
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
                    st.info("Tente novamente em alguns segundos.")

# Mostrar resultado
if st.session_state.analysis_complete and 'analysis_result' in st.session_state:
    result = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("## 📊 Sua Análise Completa e Detalhada")
    
    overall_score = result.get('overall_score', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{overall_score}/100</div><div class="stat-label">Score Geral</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">+{100-overall_score}%</div><div class="stat-label">Potencial</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(result.get("priority_actions",[]))}</div><div class="stat-label">Ações</div></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Análise Detalhada por Dimensão")
    st.markdown("*Análises completas com passos práticos de como melhorar no LinkedIn*")
    
    for dim_name, dim_data in result.get('dimensions', {}).items():
        score = dim_data['score']
        badge_class = "score-excellent" if score >= 80 else "score-good" if score >= 60 else "score-needs-work"
        status = "Excelente! ✨" if score >= 80 else "Bom, pode melhorar 💪" if score >= 60 else "Precisa Atenção 🎯"
        
        st.markdown(f"""
        <div class="dimension-card">
            <div class="dimension-title">{dim_data['icon']} {dim_data['title']}</div>
            <span class="score-badge {badge_class}">{score}/100 - {status}</span>
            <div class="dimension-content">
                {dim_data['detailed_analysis']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ✅ Plano de Ação Prioritário")
    st.markdown("*Execute nesta ordem para máximo impacto. Cada ação inclui passo-a-passo completo.*")
    
    for i, action in enumerate(result.get('priority_actions', []), 1):
        impact_badge = "score-excellent" if action['impact']=='Alto' else "score-good"
        st.markdown(f"""
        <div class="dimension-card">
            <strong style="color:#6366f1;font-size:1.1rem">{i}. {action['action']}</strong>
            <span class="score-badge {impact_badge}">{action['impact']} Impacto</span>
            <div class="dimension-content" style="margin-top:1.5rem">
                {action['how_to']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download
    download_content = f"# Análise LinkedPro - Completa\n\n## Score Geral: {overall_score}/100\n\n"
    for dim_name, dim_data in result.get('dimensions', {}).items():
        analysis_text = dim_data['detailed_analysis'].replace('<p>', '\n').replace('</p>', '\n').replace('<strong>', '**').replace('</strong>', '**').replace('<br>', '\n')
        download_content += f"\n## {dim_data['title']} ({dim_data['score']}/100)\n\n{analysis_text}\n\n"
    
    st.download_button("📄 Baixar Análise Completa", download_content, f"linkedin_analysis_{datetime.now().strftime('%Y%m%d')}.md", "text/markdown", use_container_width=True)
    
    if st.button("🔄 Analisar Outro Perfil", use_container_width=True):
        st.session_state.analysis_complete = False
        st.rerun()

# Seção Projetos
st.markdown('<div class="projects-section"><h2 class="projects-title">🚀 Outros Projetos</h2></div>', unsafe_allow_html=True)

icon_html = f'<img src="data:image/png;base64,{zen_icon}" class="project-icon">' if zen_icon else '<div class="project-icon" style="background:linear-gradient(135deg,#4f46e5,#6366f1);display:flex;align-items:center;justify-content:center;font-size:2rem">⏱️</div>'

st.markdown(f"""
<a href="https://zenoffice.netlify.app" target="_blank" style="text-decoration:none">
    <div class="project-card">
        {icon_html}
        <div class="project-info">
            <div class="project-name">ZenOffice</div>
            <div class="project-description">
                App de produtividade focado em bem-estar. Timer Pomodoro, tarefas, sons ambientes e respiração guiada.
            </div>
        </div>
    </div>
</a>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.875rem;padding:2rem 0;margin-top:2rem;border-top:1px solid rgba(255,255,255,0.1)">
    <p style="margin-bottom:0.5rem"> 100% Gratuito • Seus dados são privados</p>
    <p>Desenvolvido por <a href="https://github.com/schenkel94" target="_blank" style="color:#6366f1;text-decoration:none;font-weight:500;transition:color 0.2s">Mário Schenkel</a></p>
</div>
""", unsafe_allow_html=True)

# Cookie Notice (se não aceitou ainda)
if not st.session_state.cookies_accepted:
    cookie_container = st.container()
    with cookie_container:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**🍪 Utilizamos armazenamento local** para salvar seu progresso. Sem rastreamento, sem anúncios.")
        with col2:
            if st.button("Aceitar", key="accept_cookies", use_container_width=True):
                st.session_state.cookies_accepted = True
                st.rerun()

# Botão Flutuante de Café - FIXO e Sempre Visível
profile_html = f'<img src="data:image/png;base64,{profile_img}" style="width:100px;height:100px;border-radius:50%;margin:0 auto 1rem;display:block;border:3px solid rgba(99,102,241,0.3)">' if profile_img else ''
qr_html = f'<img src="data:image/png;base64,{qr_img}" style="width:100%">' if qr_img else '<div style="text-align:center;color:#64748b">QR Code</div>'

floating_button_html = f"""
<div id="floating-cafe" style="position:fixed;bottom:2rem;right:2rem;z-index:9999">
    <div id="cafe-btn" onclick="toggleModal()" style="width:56px;height:56px;background:linear-gradient(135deg,#f59e0b,#d97706);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(245,158,11,0.4);cursor:pointer;transition:all 0.3s;border:2px solid rgba(255,255,255,0.2);animation:pulse 2s infinite;font-size:1.5rem">
        ☕
    </div>
    
    <div id="cafe-modal" style="display:none;position:fixed;bottom:5rem;right:2rem;width:360px;max-height:600px;background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:20px;border:1px solid rgba(255,255,255,0.1);box-shadow:0 24px 64px rgba(0,0,0,0.6);overflow:hidden;animation:slideUp 0.3s">
        <div style="display:flex;border-bottom:1px solid rgba(255,255,255,0.1);padding:0.5rem">
            <div id="tab-apoiar" class="modal-tab active" onclick="switchTab('apoiar')" style="flex:1;padding:0.75rem;text-align:center;font-weight:600;font-size:0.875rem;color:#6366f1;cursor:pointer;border-bottom:2px solid #6366f1;transition:all 0.2s">APOIAR</div>
            <div id="tab-sobre" class="modal-tab" onclick="switchTab('sobre')" style="flex:1;padding:0.75rem;text-align:center;font-weight:600;font-size:0.875rem;color:#64748b;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.2s">SOBRE</div>
        </div>
        
        <div style="padding:2rem;text-align:center;max-height:500px;overflow-y:auto">
            <div id="content-apoiar">
                <div style="font-size:2.5rem;margin-bottom:1rem">☕</div>
                <h3 style="color:white;margin-bottom:0.5rem;font-size:1.25rem">Café pro Desenvolvedor?</h3>
                <p style="color:#94a3b8;font-size:0.875rem;margin-bottom:1.5rem">Ajude a manter o projeto no ar!</p>
                <div style="background:white;padding:1rem;border-radius:12px;margin:1rem auto;max-width:200px">{qr_html}</div>
                <div id="pix-key" onclick="copyPixKey()" style="background:rgba(255,255,255,0.05);padding:0.75rem;border-radius:8px;font-family:monospace;font-size:0.7rem;color:#94a3b8;word-break:break-all;margin-top:1rem;cursor:pointer;transition:all 0.2s;border:1px solid transparent" onmouseover="this.style.borderColor='rgba(99,102,241,0.5)';this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.borderColor='transparent';this.style.background='rgba(255,255,255,0.05)'">
                    df15a204-0a95-45da-8df5-c63ae7e9022e
                </div>
                <p id="copy-feedback" style="color:#10b981;font-size:0.75rem;margin-top:0.5rem;opacity:0;transition:opacity 0.3s">✓ Chave copiada!</p>
            </div>
            
            <div id="content-sobre" style="display:none">
                {profile_html}
                <h3 style="color:white;margin-bottom:0.5rem;font-size:1.25rem">Mário Schenkel</h3>
                <p style="color:#94a3b8;font-size:0.875rem;margin-bottom:1rem">Criador do ZenOffice</p>
                <p style="color:#cbd5e1;font-size:0.875rem;line-height:1.6;margin-bottom:1.5rem">Focado em criar soluções que trazem paz e produtividade.</p>
                <a href="https://linkedin.com/in/marioschenkel" target="_blank" style="background:linear-gradient(135deg,#4f46e5,#6366f1);color:white;padding:0.75rem 2rem;border-radius:12px;text-decoration:none;display:inline-block;font-weight:600;border:1px solid rgba(255,255,255,0.1);margin-bottom:0.5rem">LinkedIn</a>
                <br>
                <a href="https://github.com/schenkel94" target="_blank" style="color:#94a3b8;font-size:0.875rem;text-decoration:none;transition:color 0.2s" onmouseover="this.style.color='#6366f1'" onmouseout="this.style.color='#94a3b8'">GitHub →</a>
            </div>
        </div>
    </div>
</div>

<style>
@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 8px 24px rgba(245,158,11,0.4); }}
    50% {{ box-shadow: 0 8px 32px rgba(245,158,11,0.6); }}
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

#cafe-btn:hover {{
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 12px 32px rgba(245,158,11,0.5);
}}
</style>

<script>
function toggleModal() {{
    const modal = document.getElementById('cafe-modal');
    modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
}}

function switchTab(tab) {{
    document.querySelectorAll('.modal-tab').forEach(t => {{
        t.style.color = '#64748b';
        t.style.borderBottomColor = 'transparent';
    }});
    
    const activeTab = document.getElementById('tab-' + tab);
    activeTab.style.color = '#6366f1';
    activeTab.style.borderBottomColor = '#6366f1';
    
    document.getElementById('content-apoiar').style.display = tab === 'apoiar' ? 'block' : 'none';
    document.getElementById('content-sobre').style.display = tab === 'sobre' ? 'block' : 'none';
}}

function copyPixKey() {{
    const pixKey = 'df15a204-0a95-45da-8df5-c63ae7e9022e';
    navigator.clipboard.writeText(pixKey).then(() => {{
        const feedback = document.getElementById('copy-feedback');
        feedback.style.opacity = '1';
        setTimeout(() => {{
            feedback.style.opacity = '0';
        }}, 2000);
    }});
}}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {{
    const modal = document.getElementById('cafe-modal');
    const btn = document.getElementById('cafe-btn');
    const cafeContainer = document.getElementById('floating-cafe');
    
    if (modal.style.display === 'block' && 
        !cafeContainer.contains(event.target)) {{
        modal.style.display = 'none';
    }}
}});
</script>
"""

components.html(floating_button_html, height=0)

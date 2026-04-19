import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Revisão NBR 13484 - TOTVS", layout="wide")

# --- ESTILIZAÇÃO CSS AVANÇADA ---
st.markdown("""
    <style>
    /* 1. Bloqueio de interação em áreas de leitura (Textos e Títulos) */
    h1, h2, h3, p, span, .stMarkdown, .stCaption {
        pointer-events: none; /* O mouse 'atravessa' esses elementos */
        user-select: none;    /* Impede selecionar o texto */
    }

    /* 2. Reabilita interação apenas nos inputs e botões */
    .stButton, .stNumberInput, .stSelectbox, .stTextInput, .stPopover, button, input {
        pointer-events: auto !important;
    }

    /* 3. Moldura para a Seção de Identificação */
    [data-testid="stSidebar"] .sidebar-content {
        padding: 10px;
    }
    .sidebar-box {
        border: 1px solid #d1d1d1;
        padding: 15px;
        border-radius: 8px;
        background-color: #ffffff;
        pointer-events: auto !important;
    }

    /* 4. Garantir que o Logo apareça no topo da sidebar */
    [data-testid="stSidebarNav"] {
        display: none; /* Esconde menu padrão para focar no logo */
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS ---
@st.cache_data
def carregar_produtos():
    return pd.DataFrame([
        {"Código do Produto": "X1000676218", "Texto breve material": "CDROPAC II 5098 PROF 1A G1 100", "Família": "30", "Artigo": "86316", "Característica": "11", "Classificação": "01", "Acabamento": "00", "Embalagem": "32", "Cor": "5098", "Unida": "KG"},
        {"Código do Produto": "X1000676982", "Texto breve material": "CDROPAC II 5098 PROF 1A SANFO", "Família": "30", "Artigo": "86316", "Característica": "11", "Classificação": "01", "Acabamento": "BC", "Embalagem": "RL", "Cor": "5098", "Unida": "KG"},
        {"Código do Produto": "X1000676856", "Texto breve material": "CDROPAC II 5098 PROF 1A ACANY", "Família": "30", "Artigo": "86316", "Característica": "11", "Classificação": "01", "Acabamento": "NY", "Embalagem": "RL", "Cor": "5098", "Unida": "KG"},
        {"Código do Produto": "X1002359101", "Texto breve material": "CDROPAC II 5098 PROF 1A TINBG R", "Família": "30", "Artigo": "86316", "Característica": "11", "Classificação": "01", "Acabamento": "BG", "Embalagem": "32", "Cor": "5098", "Unida": "KG"},
        {"Código do Produto": "1000676859", "Texto breve material": "CDROPAC II MERC 1A MERAF RL", "Família": "30", "Artigo": "86316", "Característica": "19", "Classificação": "01", "Acabamento": "AF", "Embalagem": "RL", "Cor": "0000", "Unida": "KG"},
        {"Código do Produto": "1000676845", "Texto breve material": "CDROPAC II PT 1A ALVEJ RLE", "Família": "30", "Artigo": "86316", "Característica": "09", "Classificação": "01", "Acabamento": "AH", "Embalagem": "RL", "Cor": "0000", "Unida": "KG"},
    ])

df_produtos = carregar_produtos()

# --- ESTADO DA SESSÃO ---
if 'defeitos' not in st.session_state: st.session_state.defeitos = []
if 'historico' not in st.session_state: st.session_state.historico = []
if 'last_product' not in st.session_state: st.session_state.last_product = ""

# --- BARRA LATERAL ---
with st.sidebar:
    # LOGO TOTVS (Link estável)
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/59/TOTVS.svg", width=180)
    
    # Popup de Configuração
    with st.popover("⚙️ Ajustar Limites IP"):
        limite_1a = st.number_input("Limite 1ª Qualidade", value=20.0)
        limite_2a = st.number_input("Limite 2ª Qualidade", value=40.0)
    
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.subheader("Identificação do Lote")
    
    cod_selecionado = st.selectbox("Código do Produto", df_produtos["Código do Produto"].tolist())
    
    if cod_selecionado != st.session_state.last_product:
        st.session_state.defeitos = []
        st.session_state.last_product = cod_selecionado

    dados_prod = df_produtos[df_produtos["Código do Produto"] == cod_selecionado].iloc[0]
    
    st.text_input("Descrição", dados_prod["Texto breve material"], disabled=True)
    st.text_input("Família/Artigo", f"{dados_prod['Família']} / {dados_prod['Artigo']}", disabled=True)
    st.text_input("Cor/Acabamento", f"{dados_prod['Cor']} / {dados_prod['Acabamento']}", disabled=True)
    largura = st.number_input("Largura Útil (cm)", value=160.0)
    comprimento = st.number_input("Comprimento (m)", value=50.0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL (FOCO EM ENTRADA DE DADOS) ---
st.header("Sistema de Inspeção de Qualidade")
st.subheader("Revisão de Tecidos Planos - NBR 13484")

col_input, col_view = st.columns([1, 1.5])

with col_input:
    metro = st.number_input("Posição (Metro)", min_value=0.0, step=0.1)
    tipo = st.selectbox("Tipo de Defeito", ["Trama", "Urdume", "Mancha", "Furo", "Ourela"])
    
    btn_col = st.columns(4)
    if btn_col[0].button("1 Pt"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 1})
    if btn_col[1].button("2 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 2})
    if btn_col[2].button("3 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 3})
    if btn_col[3].button("4 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 4})
    
    if st.button("Desfazer Último"):
        if st.session_state.defeitos: st.session_state.defeitos.pop()

with col_view:
    if st.session_state.defeitos:
        total_pts = sum(d['Pontos'] for d in st.session_state.defeitos)
        st.table(pd.DataFrame(st.session_state.defeitos))
    else:
        st.info("Utilize os campos ao lado para registrar defeitos.")
        total_pts = 0

# --- CÁLCULO E CLASSIFICAÇÃO ---
ip = (total_pts * 100000) / (largura * comprimento) if (largura * comprimento) > 0 else 0

if ip <= limite_1a: 
    status, cor = "1ª QUALIDADE", "#28a745"
elif ip <= limite_2a: 
    status, cor = "2ª QUALIDADE", "#ffc107"
else: 
    status, cor = "REPROVADO", "#dc3545"

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Total de Pontos", f"{total_pts} pts")
c2.metric("Índice (IP)", f"{ip:.2f}")
c3.markdown(f"**Classificação:** <br> <span style='font-size:24px; color:{cor}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)

# --- RELATÓRIOS ---
st.divider()
st.subheader("Gerar Relatórios")

if st.button("Finalizar e Salvar Inspeção"):
    registro = dados_prod.to_dict()
    registro.update({"IP": round(ip, 2), "Resultado": status, "Total Pts": total_pts})
    st.session_state.historico.append(registro)
    st.success("Inspeção arquivada!")

if st.session_state.historico:
    st.dataframe(pd.DataFrame(st.session_state.historico), use_container_width=True)
    if st.button("Limpar Histórico"):
        st.session_state.historico = []
        st.rerun()

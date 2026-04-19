import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Revisão NBR 13484 - TOTVS", layout="wide")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    /* Estilização do Texto TOTVS */
    .totvs-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 40px;
        color: #002d5e;
        letter-spacing: -3px;
        font-weight: 900;
        margin-bottom: 10px;
        pointer-events: none;
    }

    /* Restrição de Cursor: impede interação em textos de leitura */
    h1, h2, h3, h4, p, span, .stMarkdown, .stCaption, .totvs-text {
        pointer-events: none;
        user-select: none;
    }

    /* Libera interação apenas para componentes de entrada */
    .stButton, .stNumberInput, .stSelectbox, .stTextInput, .stPopover, button, input, [data-testid="stTable"] {
        pointer-events: auto !important;
    }

    /* Moldura apenas na Identificação do Lote */
    .sidebar-box {
        border: 1px solid #d1d1d1;
        padding: 15px;
        border-radius: 8px;
        background-color: #ffffff;
        pointer-events: auto !important;
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

# --- INICIALIZAÇÃO DO HISTÓRICO GLOBAL (Persistente) ---
if 'historico_acumulado' not in st.session_state:
    st.session_state.historico_acumulado = []

# --- ESTADO DA INSPEÇÃO ATUAL (Limpa ao trocar produto) ---
if 'defeitos_atuais' not in st.session_state:
    st.session_state.defeitos_atuais = []
if 'last_product' not in st.session_state:
    st.session_state.last_product = ""

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<div class="totvs-text">TOTVS</div>', unsafe_allow_html=True)
    
    with st.popover("⚙️ Configurar Limites IP"):
        l1 = st.number_input("Máx 1ª Qualidade", value=20.0)
        l2 = st.number_input("Máx 2ª Qualidade", value=40.0)
    
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.subheader("Identificação do Lote")
    
    cod_selecionado = st.selectbox("Código do Produto", df_produtos["Código do Produto"].tolist())
    
    # Ao trocar o produto, limpamos apenas os dados da revisão em curso (tela central)
    if cod_selecionado != st.session_state.last_product:
        st.session_state.defeitos_atuais = []
        st.session_state.last_product = cod_selecionado

    dados_prod = df_produtos[df_produtos["Código do Produto"] == cod_selecionado].iloc[0]
    st.text_input("Descrição", dados_prod["Texto breve material"], disabled=True)
    largura = st.number_input("Largura Útil (cm)", value=160.0)
    comprimento = st.number_input("Comprimento (m)", value=50.0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Sistema de Inspeção NBR 13484")

# Seção de Entrada de Defeitos
col_in, col_tab = st.columns([1, 1.5])
with col_in:
    st.subheader("Registro de Defeitos")
    pos = st.number_input("Posição (Metro)", min_value=0.0, step=0.1)
    tipo = st.selectbox("Tipo", ["Trama", "Urdume", "Mancha", "Furo", "Ourela"])
    
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("1 Pt"): st.session_state.defeitos_atuais.append({"Metro": pos, "Tipo": tipo, "Pts": 1})
    if c2.button("2 Pts"): st.session_state.defeitos_atuais.append({"Metro": pos, "Tipo": tipo, "Pts": 2})
    if c3.button("3 Pts"): st.session_state.defeitos_atuais.append({"Metro": pos, "Tipo": tipo, "Pts": 3})
    if c4.button("4 Pts"): st.session_state.defeitos_atuais.append({"Metro": pos, "Tipo": tipo, "Pts": 4})
    
    if st.button("Remover Último"):
        if st.session_state.defeitos_atuais: st.session_state.defeitos_atuais.pop()

with col_tab:
    if st.session_state.defeitos_atuais:
        df_obs = pd.DataFrame(st.session_state.defeitos_atuais)
        st.table(df_obs)
        total_pontos = df_obs["Pts"].sum()
    else:
        st.info("Aguardando dados...")
        total_pontos = 0

# Classificação em Tempo Real
ip = (total_pontos * 100000) / (largura * comprimento) if (largura * comprimento) > 0 else 0
if ip <= l1: res, cor = "1ª QUALIDADE", "green"
elif ip <= l2: res, cor = "2ª QUALIDADE", "orange"
else: res, cor = "REPROVADO", "red"

st.divider()
st.markdown(f"**IP Atual:** {ip:.2f} | **Classificação:** :{cor}[{res}]")

# --- SEÇÃO DE RELATÓRIO (ACUMULADO) ---
st.subheader("Gerar Relatórios")

if st.button("FINALIZAR E ARMAZENAR NO RELATÓRIO"):
    # Criar o registro completo da inspeção
    registro_completo = {
        "Cód. Produto": cod_selecionado,
        "Descrição": dados_prod["Texto breve material"],
        "Total Pts": total_pontos,
        "IP Final": round(ip, 2),
        "Classificação": res,
        "Metragem": comprimento,
        "Artigo": dados_prod["Artigo"]
    }
    # Adicionar à lista persistente
    st.session_state.historico_acumulado.append(registro_completo)
    st.success(f"Inspeção do produto {cod_selecionado} arquivada com sucesso!")

# Exibição de TODAS as revisões feitas na sessão
if st.session_state.historico_acumulado:
    st.write("### Revisões Acumuladas (Todos os Produtos)")
    df_final = pd.DataFrame(st.session_state.historico_acumulado)
    st.dataframe(df_final, use_container_width=True)
    
    if st.button("Limpar Todo o Histórico"):
        st.session_state.historico_acumulado = []
        st.rerun()

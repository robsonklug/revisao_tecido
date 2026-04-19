import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Sistema de Revisão NBR 13484", layout="wide")

# --- ESTILIZAÇÃO CSS (MOLDURAS E LOGO) ---
st.markdown("""
    <style>
    /* Estilo para as molduras das colunas e seções */
    .stColumn {
        border: 1px solid #e6e9ef;
        padding: 20px;
        border-radius: 5px;
        background-color: #fcfcfc;
    }
    /* Estilo para o Logo na Barra Lateral */
    [data-testid="stSidebarNav"]::before {
        content: "TOTVS";
        margin-left: 20px;
        margin-top: 20px;
        font-size: 30px;
        font-weight: bold;
        color: #004a99; /* Azul TOTVS */
        font-family: sans-serif;
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
if 'defeitos' not in st.session_state:
    st.session_state.defeitos = []
if 'historico_inspecoes' not in st.session_state:
    st.session_state.historico_inspecoes = []
if 'last_product' not in st.session_state:
    st.session_state.last_product = ""

# --- BARRA LATERAL ---
# Simulando o Logo TOTVS via imagem ou texto estilizado
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/TOTVS.svg/1280px-TOTVS.svg.png", width=150)
st.sidebar.markdown("### Identificação do Lote")

cod_selecionado = st.sidebar.selectbox("Selecione o Código do Produto", df_produtos["Código do Produto"].tolist())

if cod_selecionado != st.session_state.last_product:
    st.session_state.defeitos = []
    st.session_state.last_product = cod_selecionado

dados_prod = df_produtos[df_produtos["Código do Produto"] == cod_selecionado].iloc[0]

st.sidebar.text_input("Descrição", dados_prod["Texto breve material"], disabled=True)
st.sidebar.text_input("Família/Artigo", f"{dados_prod['Família']} / {dados_prod['Artigo']}", disabled=True)
st.sidebar.text_input("Cor/Acabamento", f"{dados_prod['Cor']} / {dados_prod['Acabamento']}", disabled=True)
largura = st.sidebar.number_input("Largura Útil (cm)", value=160.0)
comprimento = st.sidebar.number_input("Comprimento do Rolo (m)", value=50.0)

# --- CORPO PRINCIPAL ---
st.title("Revisão de Tecidos Planos - NBR 13484")
st.caption(f"Inspecionando: {cod_selecionado} - {dados_prod['Texto breve material']}")

# Colunas com bordas simuladas por container
with st.container():
    col_add, col_map = st.columns([1, 1.5], gap="large")

    with col_add:
        st.subheader("Adicionar Defeito")
        metro = st.number_input("Posição (Metro)", min_value=0.0, step=0.1)
        tipo = st.selectbox("Tipo", ["Trama", "Urdume", "Mancha", "Furo", "Ourela"])
        
        pts_col = st.columns(4)
        if pts_col[0].button("1 Pt"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 1})
        if pts_col[1].button("2 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 2})
        if pts_col[2].button("3 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 3})
        if pts_col[3].button("4 Pts"): st.session_state.defeitos.append({"Metro": metro, "Tipo": tipo, "Pontos": 4})
        
        if st.button("Remover Último"):
            if st.session_state.defeitos: st.session_state.defeitos.pop()

    with col_map:
        st.subheader("Mapa de Defeitos Atual")
        if st.session_state.defeitos:
            st.table(pd.DataFrame(st.session_state.defeitos))
            total_pontos = sum(d['Pontos'] for d in st.session_state.defeitos)
        else:
            st.info("Nenhum defeito registrado.")
            total_pontos = 0

# --- CÁLCULOS E RELATÓRIO ---
ip = (total_pontos * 100000) / (largura * comprimento) if (largura * comprimento) > 0 else 0
if ip <= 20: status = "PRIMEIRA QUALIDADE"
elif ip <= 40: status = "SEGUNDA QUALIDADE"
else: status = "REPROVADO"

st.divider()

if st.button("GERAR RELATÓRIO FINAL"):
    # Salvar no histórico
    nova_inspecao = dados_prod.to_dict()
    nova_inspecao.update({
        "Total Pontos": total_pontos,
        "IP": round(ip, 2),
        "Classificação": status,
        "Metragem": comprimento
    })
    st.session_state.historico_inspecoes.append(nova_inspecao)
    st.success("Inspeção finalizada e armazenada no histórico!")

# --- EXIBIÇÃO DO HISTÓRICO ACUMULADO ---
if st.session_state.historico_inspecoes:
    st.header("Relatório de Inspeções Realizadas (Histórico)")
    df_hist = pd.DataFrame(st.session_state.historico_inspecoes)
    
    # Reorganizando colunas para facilitar leitura
    colunas_ordem = ["Código do Produto", "Texto breve material", "Metragem", "Total Pontos", "IP", "Classificação"]
    # Adicionando as outras colunas técnicas no final
    outras_cols = [c for c in df_hist.columns if c not in colunas_ordem]
    st.dataframe(df_hist[colunas_ordem + outras_cols], use_container_width=True)

    if st.button("Limpar Todo Histórico"):
        st.session_state.historico_inspecoes = []
        st.rerun()

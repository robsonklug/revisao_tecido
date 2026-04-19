import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Sistema de Revisão NBR 13484", layout="wide")

# --- BASE DE DADOS (Extraída da imagem enviada) ---
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
if 'last_product' not in st.session_state:
    st.session_state.last_product = ""

# --- BARRA LATERAL: SELEÇÃO E IDENTIFICAÇÃO ---
st.sidebar.header("Identificação do Lote")

# Seleção do Código
cod_selecionado = st.sidebar.selectbox("Selecione o Código do Produto", df_produtos["Código do Produto"].tolist())

# Resetar inspeção se o produto mudar
if cod_selecionado != st.session_state.last_product:
    st.session_state.defeitos = []
    st.session_state.last_product = cod_selecionado

# Filtrar dados do produto selecionado
dados_prod = df_produtos[df_produtos["Código do Produto"] == cod_selecionado].iloc[0]

# Exibição dos dados (Somente Leitura)
st.sidebar.text_input("Descrição", dados_prod["Texto breve material"], disabled=True)
st.sidebar.text_input("Família/Artigo", f"{dados_prod['Família']} / {dados_prod['Artigo']}", disabled=True)
st.sidebar.text_input("Cor/Acabamento", f"{dados_prod['Cor']} / {dados_prod['Acabamento']}", disabled=True)

# Dados de entrada da inspeção
largura = st.sidebar.number_input("Largura Útil (cm)", value=160.0, step=1.0)
comprimento = st.sidebar.number_input("Comprimento do Rolo (m)", value=50.0, step=1.0)

# --- CORPO PRINCIPAL ---
st.title("Revisão de Tecidos Planos - NBR 13484")
st.write(f"Inspecionando: **{cod_selecionado} - {dados_prod['Texto breve material']}**")

col_add, col_map = st.columns([1, 2])

with col_add:
    st.subheader("Adicionar Defeito")
    metro = st.number_input("Posição (Metro)", min_value=0.0, step=0.1)
    tipo = st.selectbox("Tipo", ["Trama", "Urdume", "Mancha", "Furo", "Ourela"])
    
    # Sistema de botões limpos
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
        df_obs = pd.DataFrame(st.session_state.defeitos)
        st.table(df_obs) # Table é mais limpo que dataframe para relatórios
        total_pontos = df_obs["Pontos"].sum()
    else:
        st.write("Aguardando registros...")
        total_pontos = 0

# --- CÁLCULOS ---
ip = (total_pontos * 100000) / (largura * comprimento) if (largura * comprimento) > 0 else 0

if ip <= 20: status = "PRIMEIRA QUALIDADE"
elif ip <= 40: status = "SEGUNDA QUALIDADE"
else: status = "REPROVADO"

st.divider()

# --- RELATÓRIO EM TELA ---
if st.button("GERAR RELATÓRIO FINAL"):
    st.subheader("Relatório de Inspeção Consolidado")
    
    # Criando o dicionário do relatório com os dados da planilha + resultados
    relatorio_data = dados_prod.to_dict()
    relatorio_data.update({
        "Largura (cm)": largura,
        "Comprimento (m)": comprimento,
        "Total Pontos": total_pontos,
        "Índice de Pontos (IP)": f"{ip:.2f}",
        "Classificação Final": status
    })
    
    df_relatorio = pd.DataFrame([relatorio_data])
    st.dataframe(df_relatorio)
    
    # Detalhamento dos defeitos no relatório
    if st.session_state.defeitos:
        st.write("**Detalhamento dos Defeitos Encontrados:**")
        st.table(pd.DataFrame(st.session_state.defeitos))

# Métricas de rodapé para auxílio visual rápido
m1, m2, m3 = st.columns(3)
m1.metric("Total de Pontos", total_pontos)
m2.metric("IP (Pts/100m²)", f"{ip:.2f}")
m3.metric("Status", status)

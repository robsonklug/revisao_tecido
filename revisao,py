import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Revisão de Tecidos - NBR 13484", layout="wide")

# Inicialização do estado da sessão para armazenar defeitos
if 'defeitos_lista' not in st.session_state:
    st.session_state.defeitos_lista = []

def calcular_ip(total_pontos, largura, comprimento):
    if largura > 0 and comprimento > 0:
        # Fórmula: (Pontos * 100.000) / (Largura(cm) * Comprimento(m))
        return (total_pontos * 100000) / (largura * comprimento)
    return 0

# --- ESTRUTURA LATERAL (IDENTIFICAÇÃO) ---
st.sidebar.header("📋 Identificação do Lote")
cod_produto = st.sidebar.text_input("Código do Produto", "X1000676218")
desc_produto = st.sidebar.text_area("Descrição", "CDROPAC II 5098 PROF 1A G1 100")
largura_nominal = st.sidebar.number_input("Largura Útil (cm)", value=160.0)
comprimento_total = st.sidebar.number_input("Comprimento Total (m)", value=50.0)

# --- CORPO PRINCIPAL ---
st.title("🚀 Inspeção de Tecidos Planos")
st.subheader(f"Produto: {cod_produto} - {desc_produto}")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("### Adicionar Defeito")
    metragem_atual = st.number_input("Metragem do Defeito (m)", min_value=0.0, step=0.1)
    tipo_defeito = st.selectbox("Tipo de Defeito", ["Trama", "Urdume", "Mancha", "Furo", "Outros"])
    
    st.write("**Pontuação (Tamanho):**")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("1 pt"): st.session_state.defeitos_lista.append({"Metro": metragem_atual, "Tipo": tipo_defeito, "Pontos": 1})
    if c2.button("2 pts"): st.session_state.defeitos_lista.append({"Metro": metragem_atual, "Tipo": tipo_defeito, "Pontos": 2})
    if c3.button("3 pts"): st.session_state.defeitos_lista.append({"Metro": metragem_atual, "Tipo": tipo_defeito, "Pontos": 3})
    if c4.button("4 pts"): st.session_state.defeitos_lista.append({"Metro": metragem_atual, "Tipo": tipo_defeito, "Pontos": 4})

    if st.button("Limpar Último Registro"):
        if st.session_state.defeitos_lista:
            st.session_state.defeitos_lista.pop()

with col2:
    st.write("### Mapa de Defeitos")
    if st.session_state.defeitos_lista:
        df = pd.DataFrame(st.session_state.defeitos_lista)
        st.dataframe(df, use_container_width=True)
        total_pts = df['Pontos'].sum()
    else:
        st.info("Nenhum defeito registrado até o momento.")
        total_pts = 0

st.divider()

# --- RESULTADOS E CLASSIFICAÇÃO ---
st.header("📊 Resultado Final")
ip_resultado = calcular_ip(total_pts, largura_nominal, comprimento_total)

res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("Total de Pontos", f"{total_pts} pts")
res_col2.metric("Índice de Pontos (IP)", f"{ip_resultado:.2f}")

# Critério de Classificação Sugerido (Pode ser ajustado conforme a tecelagem)
if ip_resultado <= 20:
    status = "PRIMEIRA QUALIDADE"
    cor = "green"
elif ip_resultado <= 40:
    status = "SEGUNDA QUALIDADE"
    cor = "orange"
else:
    status = "REPROVADO / TERCEIRA"
    cor = "red"

res_col3.markdown(f"### Classificação: <span style='color:{cor}'>{status}</span>", unsafe_allow_html=True)

# Exportação
if st.button("Gerar Relatório CSV"):
    if st.session_state.defeitos_lista:
        df.to_csv("relatorio_inspecao.csv", index=False)
        st.success("Relatório pronto para download (simulado)!")

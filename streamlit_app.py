import streamlit as st
from exemplos import exemplos  # Importe o dicionário de exemplos

# Criação do menu lateral
#st.sidebar.image("caminho_para_seu_logo.png", caption="RiscoCardioAI")
exemplo_selecionado = st.sidebar.selectbox("Exemplos", options=list(exemplos.keys()))

# Atualiza os valores dos inputs baseado no exemplo selecionado
valores_exemplo = exemplos[exemplo_selecionado]
nome = st.text_input("Nome", key="name", value=valores_exemplo["name"])
idade = st.text_input("Idade", key="idade", value=valores_exemplo["idade"], max_chars=3)

# Verificar se a idade é um número
if idade and not idade.isnumeric():
    st.error("Por favor, insira apenas números para a idade.")

prontuario = st.text_area("Prontuário", key="prontuario", height=300, value=valores_exemplo["prontuario"])
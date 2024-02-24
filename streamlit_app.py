import streamlit as st

st.text_input("Nome", key="name")

idade = st.text_input("Idade", key="idade", max_chars=3)

# Verificar se a idade é um número
if idade and not idade.isnumeric():
    st.error("Por favor, insira apenas números para a idade.")

st.text_area("Prontuário", key="prontuario", height=300)
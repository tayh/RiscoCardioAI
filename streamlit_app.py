import streamlit as st
from exemplos import exemplos
from models_load import load_ner_model
from processing_predictions import ProcessPredictions

ner_model = load_ner_model()
process_predictions = ProcessPredictions(ner_model=ner_model)
# Criação do menu lateral
st.sidebar.image("logo.png")
exemplo_selecionado = st.sidebar.selectbox("Exemplos", options=list(exemplos.keys()))

# Atualiza os valores dos inputs baseado no exemplo selecionado
valores_exemplo = exemplos[exemplo_selecionado]
nome = st.text_input("Nome", key="name", value=valores_exemplo["name"])
idade = st.text_input("Idade", key="idade", value=valores_exemplo["idade"], max_chars=3)

# Verificar se a idade é um número
if idade and not idade.isnumeric():
    st.error("Por favor, insira apenas números para a idade.")

prontuario = st.text_area("Prontuário", key="prontuario", height=300, value=valores_exemplo["prontuario"])

all_infos = process_predictions.process_all_infos(prontuario)
print(all_infos)

normalized_background_and_comorbidity = process_predictions.normalize_background_and_comorbidity(all_infos["background_and_comorbidity"])
print(normalized_background_and_comorbidity)
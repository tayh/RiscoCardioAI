import streamlit as st
from exemplos import exemplos
from models_load import load_ner_model, load_postagger_model
from processing_predictions import ProcessPredictions

st.set_page_config(
     page_title='RiscoCardioAI',
     layout="wide",
     initial_sidebar_state="expanded",
)

ner_model = load_ner_model()
ner_postagger = load_postagger_model()
process_predictions = ProcessPredictions(ner_model=ner_model, ner_postagger=ner_postagger)

# Criação do menu lateral para seleção de exemplos
st.sidebar.image("logo.png")
exemplo_selecionado = st.sidebar.selectbox("Exemplos", options=list(exemplos.keys()))

st.markdown("### Preencha o formulário")
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

# Definição das cores para as condições presentes
cores = ["#270240", "#150359", "#0511F2", "#30BFBF", "#0D0D0D"]
condicoes = all_infos.get('present_conditions', [])

# Exibição das condições presentes com cores específicas
st.markdown("#### Condições Presentes")
for i, condicao in enumerate(condicoes):
    cor = cores[i % len(cores)]  # Garante que a lista de cores seja reutilizada se necessário
    # Utiliza HTML personalizado para exibir cada condição com a cor especificada
    st.markdown(f"<div style='color: {cor};'>{condicao}</div>", unsafe_allow_html=True)

st.markdown("#### Histórico familiar")
st.markdown(all_infos.get('family_history', None))
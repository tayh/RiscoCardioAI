import streamlit as st
from exemplos import exemplos
from models_load import load_ner_model, load_postagger_model
from processing_predictions import ProcessPredictions
from framinghamscore import FraminghamScore
import re

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

# Início da criação das colunas
col_form, col_infos = st.columns(2, gap="medium")
framingham_score = FraminghamScore()

def convert_to_float(text):
    # Regex para identificar números que podem conter pontos e vírgulas
    # A regex abaixo considera tanto formatos com ponto quanto com vírgula como separador decimal.
    # Ela não captura números em formato 1,000.00 (milhar com vírgula e decimal com ponto)
    # pois há ambiguidade em diferentes padrões culturais (ex: 1.000,00 em alguns países é mil).
    pattern = r'\d+[,.]?\d*'

    # Encontrar todos os números no texto
    matches = re.findall(pattern, text)

    if not matches:
        return 0

    # Converter os números para float
    standardized_number = 0
    for match in matches:
        # Substituir vírgulas por pontos para padronização
        standardized_number = match.replace(',', '.')
        # Converter para float e adicionar à lista   
    return standardized_number

with col_form:
    st.markdown("### Preencha o formulário")
    # Atualiza os valores dos inputs baseado no exemplo selecionado
    valores_exemplo = exemplos[exemplo_selecionado]
    nome = st.text_input("Nome", key="name", value=valores_exemplo["name"])
    idade = st.text_input("Idade", key="idade", value=valores_exemplo["idade"], max_chars=3)
    sexo = st.radio('Sexo:', ['F', 'M'], index=['F', 'M'].index(valores_exemplo["sexo"]))

    # Verificar se a idade é um número
    if idade and not idade.isnumeric():
        st.error("Por favor, insira apenas números para a idade.")

    prontuario = st.text_area("Prontuário", key="prontuario", height=300, value=valores_exemplo["prontuario"])
    
    # Botão de enviar
    enviado = st.button("Enviar")

if enviado:  # Processa as informações apenas se o botão for clicado
    with col_infos:
        st.markdown("### Informações encontradas")
        if prontuario:  # Garante que as informações sejam processadas apenas se houver prontuário
            all_infos = process_predictions.process_all_infos(prontuario)
            # Definição das cores para as condições presentes
            cores = ["#270240", "#150359", "#0511F2", "#30BFBF", "#0D0D0D"]
            condicoes = all_infos.get('present_conditions', [])

            st.markdown("##### Framingham Risk Score")
            pa_category = all_infos.get("blood_pressure_category")
            colesterol_total = convert_to_float(all_infos.get("colesterol"))
            hdl = convert_to_float(all_infos.get("hdl"))
            smoker = all_infos.get("smoker")
            diabetic = all_infos.get("diabetic")
            score = framingham_score.calculate_framingham_score(
                total_cholesterol=float(colesterol_total),
                age=int(idade),
                hdl=float(hdl),
                diabetic=diabetic,
                smoker=smoker,
                gender=sexo,
                blood_pressure=pa_category
            )
            st.markdown("* " + str(score))

            # Exibição das condições presentes com cores específicas
            st.markdown("##### Fatores de risco encontrados:")
            for i, condicao in enumerate(condicoes):
                st.markdown("* " + str(condicao))
            
            st.markdown("##### Antecedentes e comorbidades:")
            st.markdown(all_infos.get('background_and_comorbidity', None))

            #st.markdown("#### Outros")
            medicaments_tab, exams_tab, imc_tab, pa_tab, af_tab = st.tabs(["Medicamentos", "Exames", "IMC", "Pressão Arterial", "Antecedentes Familiares"])
            with medicaments_tab:
                diabetes_medicamentos = all_infos.get('diabetes_medicaments', [])
                has_medicamentos = all_infos.get('has_medicaments', [])
                dlp_medicamentos = all_infos.get('dlp_medicaments', [])
                if diabetes_medicamentos:
                    st.markdown("###### Medicamentos de diabetes:")
                    for i, medicamento in enumerate(diabetes_medicamentos):
                        st.markdown("* " + medicamento.upper())
                if has_medicamentos:
                    st.markdown("###### Medicamentos de hipertensão:")
                    for i, medicamento in enumerate(has_medicamentos):
                        st.markdown("* " + medicamento.upper())
                if dlp_medicamentos:
                    st.markdown("###### Medicamentos de dislipidemia:")
                    for i, medicamento in enumerate(dlp_medicamentos):
                        st.markdown("* " + medicamento.upper())
            with exams_tab:
                exames_diabetes = all_infos.get('exames_diabetes', [])
                hb_glic = all_infos.get('hba1c', [])
                glicemia = all_infos.get('glucose', [])
                exames_dlp = all_infos.get('exames_dlp', [])
                if exames_diabetes:
                    st.markdown("###### Exames de diabetes:")
                    st.markdown("* " + hb_glic.upper())
                    st.markdown("* " + glicemia.upper())
                if exames_dlp:
                    hdl = all_infos.get('hdl', [])
                    ldl = all_infos.get('ldl', [])
                    colesterol = all_infos.get('colesterol', [])
                    triglic = all_infos.get('triglic', [])
                    st.markdown("###### Exames de dislipidemia:")
                    st.markdown("* " + hdl.upper())
                    st.markdown("* " + ldl.upper())
                    st.markdown("* " + colesterol.upper())
                    st.markdown("* " + triglic.upper())

            with imc_tab:
                imc = all_infos.get('imc', [])
                if imc:
                    st.markdown("###### IMC:")
                    st.markdown("* " + imc.upper())
            with pa_tab:
                pressao_arterial = all_infos.get('blood_pressure', [])
                pa_text = all_infos.get("blood_pressure_text", "")
                if pressao_arterial:
                    for bp in pressao_arterial:
                        st.markdown("Pressão Sistólica:" + str(bp[0]))
                        st.markdown("Pressão Diastólica:" + str(bp[1]))

            with af_tab:
                st.markdown("###### Antecedentes familiares:")
                st.markdown(all_infos.get('family_history', None))

# Estilo adicional
st.markdown("""
    <style>
        [data-testid="column"]:nth-child(2){
            background-color: #ffff;
            padding-left: 10px;
        }
    </style>
    """, unsafe_allow_html=True
)

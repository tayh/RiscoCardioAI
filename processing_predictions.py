from normalization_map import vocabulary
from unidecode import unidecode
import re
from nltk import Tree
from regular_expression import REGEX_HB_GLIC

class ProcessPredictions:
    ANTECEDENTE_COMORBIDADE = 'AntecedenteComorbidade'
    HISTORICO_FAMILIAR = 'AntecedenteFamiliar'
    DIABETES_MEDICAMENTOS = 'MedicamentosDiabetes'
    HAS_MEDICAMENTOS = 'MedicamentosHAS'
    DLP_MEDICAMENTOS = 'MedicamentosDLP'
    PRESSAO_ARTERIAL = 'PressaoArterial'
    IMC = 'IMC'
    EXAMES_DIABETES = 'ExamesDiabetes'
    EXAMES_DLP = 'ExamesDLP'

    def __init__(self, ner_model, ner_postagger):
        self.ner_model = ner_model
        self.ner_postagger = ner_postagger

    def get_words_by_entity(self, data, target_entity):
        words = [item['word'] for item in data if item['entity_group'] == target_entity]
        return words

    def process_predictions(self, prontuario):
        predictions = self.ner_model(prontuario)
        return predictions

    def process_background_and_comorbidity(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.ANTECEDENTE_COMORBIDADE)
        return " ".join(result)

    def process_family_history(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.HISTORICO_FAMILIAR)
        return " ".join(result)

    def process_diabetes_medicaments(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.DIABETES_MEDICAMENTOS)
        return list(set(result))

    def process_has_medicaments(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.HAS_MEDICAMENTOS)
        return list(set(result))

    def process_dlp_medicaments(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.DLP_MEDICAMENTOS)
        return list(set(result))

    def process_blood_pressure(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.PRESSAO_ARTERIAL)
        return " ".join(result)

    def process_imc(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.IMC)
        return " ".join(result)

    def process_diabetes_exams(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.EXAMES_DIABETES)
        return " ".join(result)
    
    def process_hb_glic(self, exames):
        result = re.search(REGEX_HB_GLIC, exames, re.I)
        if result:
            return result.group()
        return ""
    
    def process_dlp_exams(self, predictions):
        result = self.get_words_by_entity(data=predictions, target_entity=self.EXAMES_DLP)
        return " ".join(result)

    def apply_grammar_rules(self, predictions):
        trees = []
        processed_indices = set()

        negation_pattern = re.compile(r'(nega|não apresenta|sem|não|nao)', re.IGNORECASE)
        conjunction_pattern = re.compile(r'(e|de)', re.IGNORECASE)
        punctuation_pattern = re.compile(r'([,.])')

        i = 0
        while i < len(predictions):
            if negation_pattern.match(predictions[i]['word']) and i not in processed_indices:
                negation_word = predictions[i]['word']
                negation_children = []
                processed_indices.add(i)
                j = i + 1

                while j < len(predictions):
                    if predictions[j]['entity_group'] == 'N' and j not in processed_indices:
                        negation_children.append(predictions[j]['word'])
                        processed_indices.add(j)
                    elif conjunction_pattern.match(predictions[j]['word']) and j + 1 < len(predictions) and predictions[j + 1]['entity_group'] == 'N':
                        # Inclui a lógica para tratar termos após a conjunção "e"
                        processed_indices.add(j)
                    elif punctuation_pattern.match(predictions[j]['word']):
                        # Para por aqui se encontrar uma pontuação que não seja parte da lista de negações
                        if predictions[j]['word'] == ',':
                            # Se for uma vírgula, apenas continua, pois pode haver mais itens na lista
                            processed_indices.add(j)
                        else:
                            # Encerra o agrupamento se for um ponto ou outra pontuação final
                            break
                    else:
                        # Encerra o agrupamento se não for uma conjunção que continua a lista de negações
                        break
                    j += 1

                if negation_children:
                    tree = Tree(negation_word, [Tree(child, []) for child in negation_children])
                    trees.append(tree)
                i = j  # Atualiza i para continuar a partir do último ponto processado
            else:
                i += 1  # Avança se a palavra atual não for uma negação ou já foi processada

        return trees

    def collect_leaves_after_node(self, tree):
        words_after_node = []
        for subtree in tree:
            word = subtree.label()
            words_after_node.append(word.lower())
        return words_after_node

    def identify_non_negated_conditions_with_postagger(self, background_and_comorbidity):
        background_and_comorbidity = background_and_comorbidity.lower()
        # Processa o texto com o POS tagger
        pos_predictions = self.ner_postagger(background_and_comorbidity)

        negated_words = []
        # Aplica as regras gramaticais para identificar negações
        negation_trees = self.apply_grammar_rules(pos_predictions)

        # Extrai as palavras negadas das árvores
        # Itera sobre cada árvore e extrai palavras negadas
        for tree in negation_trees:
            negated_words.extend(self.collect_leaves_after_node(tree))

        # Normaliza e identifica condições mapeadas em 'vocabulary'
        normalized_terms = self.normalize_background_and_comorbidity(background_and_comorbidity)
        negated_words_normalize = self.normalize_background_and_comorbidity(" ".join(negated_words))
        conditions_present = set(normalized_terms) - set(negated_words_normalize)

        return list(conditions_present)


    def normalize_background_and_comorbidity(self, background_and_comorbidity):
        normalized_terms = set()
        # Limpa e normaliza a entrada inteira
        clean_input = re.sub(r'[^\w\s]', '', background_and_comorbidity)
        clean_input = unidecode(clean_input.lower())
        
        # Encontra o comprimento máximo das chaves do vocabulário para limitar as subsequências verificadas
        max_key_length = max(len(key.split()) for key in vocabulary)
        # Divida a entrada limpa em palavras
        words = clean_input.split()
        # Cria subsequências de palavras e verifica se correspondem a uma chave do vocabulário
        for i in range(len(words)):
            for j in range(1, max_key_length + 1):
                phrase = " ".join(words[i:i+j])
                if phrase in vocabulary:
                    normalized_terms.add(vocabulary[phrase])
                    break  # Sai do loop interno se uma correspondência for encontrada
        return normalized_terms

    def check_medicaments_presence(self, diabetes_medicaments, has_medicaments, dlp_medicaments, present_conditions):
        # Inicializa o conjunto de condições presentes com as já identificadas
        merge_conditions = set(present_conditions)
        
        # Adiciona condições baseadas na presença de medicamentos
        if diabetes_medicaments:
            merge_conditions.add('Diabetes')
        if has_medicaments:
            merge_conditions.add('Hipertensão')
        if dlp_medicaments:
            merge_conditions.add('Dislipidemia')
        
        return merge_conditions

    def process_all_infos(self, prontuario):
        predictions = self.process_predictions(prontuario)
        background_and_comorbidity = self.process_background_and_comorbidity(predictions)
        family_history = self.process_family_history(predictions)
        diabetes_medicaments = self.process_diabetes_medicaments(predictions)
        has_medicaments = self.process_has_medicaments(predictions)
        dlp_medicaments = self.process_dlp_medicaments(predictions)
        blood_pressure = self.process_blood_pressure(predictions)
        imc = self.process_imc(predictions)
        exames_diabetes = self.process_diabetes_exams(predictions)
        exames_dlp = self.process_dlp_exams(predictions)
        hb_glic = self.process_hb_glic(exames_diabetes)
        print(exames_diabetes)
        print(hb_glic)
        present_conditions = self.identify_non_negated_conditions_with_postagger(background_and_comorbidity)
        final_conditions = self.check_medicaments_presence(
            diabetes_medicaments=diabetes_medicaments, 
            has_medicaments=has_medicaments, 
            dlp_medicaments=dlp_medicaments,
            present_conditions=present_conditions
        )
        return {
            "background_and_comorbidity": background_and_comorbidity,
            "family_history": family_history,
            "present_conditions": final_conditions,
            "diabetes_medicaments": diabetes_medicaments,
            "has_medicaments": has_medicaments,
            "dlp_medicaments": dlp_medicaments,
            "blood_pressure": blood_pressure,
            "imc": imc,
            "exames_diabetes": exames_diabetes,
            "exames_dlp": exames_dlp,
            "hba1c": hb_glic
        }
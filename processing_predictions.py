from normalization_map import vocabulary
from unidecode import unidecode

class ProcessPredictions:
    ANTECEDENTE_COMORBIDADE = 'AntecedenteComorbidade'
    HISTORICO_FAMILIAR = 'AntecedenteFamiliar'

    def __init__(self, ner_model):
        self.ner_model = ner_model

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

    def process_all_infos(self, prontuario):
        predictions = self.process_predictions(prontuario)
        background_and_comorbidity = self.process_background_and_comorbidity(predictions)
        family_history = self.process_family_history(predictions)
        return {
            "background_and_comorbidity": background_and_comorbidity,
            "family_history": family_history
        }

    def normalize_background_and_comorbidity(self, background_and_comorbidity):
        normalized_terms = set()
        words = background_and_comorbidity.split()
        for word in words:
            normalized_word = unidecode(word.lower())
            if normalized_word in vocabulary:
                normalized_terms.add(vocabulary[normalized_word])
        return " ".join(normalized_terms) 
from transformers import AutoTokenizer
from transformers import pipeline
import os
import logging
import spacy

MODEL_NER_PATH = os.getenv("MODEL_NER_PATH")
MODEL_TOKENIZER_PATH = os.getenv("MODEL_TOKENIZER_PATH")

def load_ner_model():
    logging.info("Carregando modelo de prontuários")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_TOKENIZER_PATH)
    ner_prontuarios = pipeline("ner", model=MODEL_NER_PATH, tokenizer=tokenizer, aggregation_strategy="first", ignore_labels=[])
    return ner_prontuarios

def load_spacy_model():
    logging.info("Carregando modelo do spacy")
    nlp = spacy.load("pt_core_news_lg")
    return nlp
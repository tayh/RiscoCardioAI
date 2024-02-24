from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
import logging
import spacy

MODEL_NER_PATH = os.getenv("MODEL_NER_PATH")
MODEL_TOKENIZER_PATH = os.getenv("MODEL_TOKENIZER_PATH")
MODEL_POSTAGGER_PATH = os.getenv("MODEL_POSTAGGER_PATH")

def load_ner_model():
    logging.info("Carregando modelo de prontuários")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_TOKENIZER_PATH)
    ner_prontuarios = pipeline("ner", model=MODEL_NER_PATH, tokenizer=tokenizer, aggregation_strategy="first", ignore_labels=[])
    return ner_prontuarios

def load_postagger_model():
     logging.info("Carregando modelo de postagger")
     tokenizer = AutoTokenizer.from_pretrained(MODEL_POSTAGGER_PATH)
     postagger = pipeline("ner", model=MODEL_POSTAGGER_PATH, tokenizer=tokenizer, aggregation_strategy="max")
     return postagger

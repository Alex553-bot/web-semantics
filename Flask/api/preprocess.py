import spacy
import re

nlp = spacy.load("es_core_news_sm")

def preprocess(s: str):
    s = remove_punctuation(s)
    doc = nlp(s)    
    processed_words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    
    return processed_words

def remove_punctuation(s: str): 
    return re.sub(r'[^\w\s]', '', s)
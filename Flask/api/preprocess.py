import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

import re

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def preprocess(s:str):
	s = remove_punctuation(s)
	words = word_tokenize(s)
	stop_words = set(stopwords.words('spanish'))
	words = [word.lower() for word in words if word.lower() not in stop_words]
	stemmer = SnowballStemmer('spanish')
	stemmed_words = [stemmer.stem(word) for word in words]
	return stemmed_words

def remove_punctuation(s:str): 
	return re.sub(r'[^\w\s]', '', s)
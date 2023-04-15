# -*- coding: utf-8 -*-

import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import collections
import re
import tabula
from nltk.stem import PorterStemmer
import json


def concatenate_word(text):
    text_lines = text.splitlines()
    
    for i in range(len(text_lines)):
        if len(text_lines[i]) == 0:
            continue
        
        if(text_lines[i][-1] ==  "-"):
            next_line_words = text_lines[i+1].split(" ")
            text_lines[i] =  text_lines[i][:-1] + next_line_words[0]
            text_lines[i+1] = ' '.join(next_line_words[1:])

    text = ''
    for i in text_lines:
        text += i
    return text
# Le todas a paginas do pdf
with open('image_processing/Going_deeper_with_convolutions.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for i in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[i]
        text += pdf_page.extract_text()
        
text = concatenate_word(text)
# Remove pontuação

text = re.sub(r'\n', ' ', text)
text = re.sub(r'[^a-zA-Z\s]', '', text)
#print(text)

# Remove as stopwords do conteúdo
stop_words = set(stopwords.words('english'))
tokens = word_tokenize(text.lower())
filtered_tokens = [token for token in tokens if token not in stop_words]



word_counts = collections.Counter(filtered_tokens)

most_common_words = word_counts.most_common(10)

# Imprime as 10 palavras mais frequentes
for word, count in most_common_words:
    print(f'{word}: {count}')

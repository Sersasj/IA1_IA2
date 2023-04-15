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

def concatenate_word():
    global text
    text_lines = text.splitlines()

    for i in range(len(text_lines)):
        if len(text_lines[i]) == 0:
            continue

        if (text_lines[i][-1] == "-"):
            next_line_words = text_lines[i+1].split(" ")
            text_lines[i] = text_lines[i][:-1] + next_line_words[0]
            text_lines[i+1] = ' '.join(next_line_words[1:])

    text = ''
    for i in text_lines:
        text += i

# realiza a limpeza dos texto
def preprocessamento():
    global text

    concatenate_word()
    
    # Remove pontuação
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # print(text)


def identificaTermos():
    
    # verifica se possui as stopword
    try:
        stopwords.words('english')
    except:
        nltk.download('stopwords')
        nltk.download('punkt')

    # Remove as stopwords do conteúdo
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words]

    word_counts = collections.Counter(filtered_tokens)

    most_common_words = word_counts.most_common(10)

    # Imprime as 10 palavras mais frequentes
    for word, count in most_common_words:
        print(f'{word}: {count}')


if __name__ == '__main__':

    # path = 'testes/Teste_2pag_Particle.pdf'
    # path = 'image_processing/Going_deeper_with_convolutions.pdf'
    path = './artificial_intelligence/Particle_swarm_optimization.pdf'
    
    # Le todas a paginas do pdf
    with open(path, 'rb') as pdf_file:
        # Cria obj de leitura do pdf
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        info = pdf_reader.metadata
        text = ''
        # for i in range(len(pdf_reader.pages)):
        for i in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[i]
            text += pdf_page.extract_text()
            # print(text)

    print('Autor(es):', info.author)
    print('Titulo:', info.title, '\n')
    
    preprocessamento()

    print(pdf_reader.pages[0])

    # identificaTermos()

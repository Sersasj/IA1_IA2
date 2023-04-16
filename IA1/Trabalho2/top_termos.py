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
import unicodedata

def concatenate_word():
    global text
    text_lines = text.splitlines()

    for i in range(len(text_lines)):
        if len(text_lines[i]) == 0:
            continue

        if (text_lines[i][-1] == "-"):
            next_line_words = text_lines[i+1].split(" ")
            text_lines[i] = text_lines[i][:-1] + next_line_words[0] + " "
            text_lines[i+1] = ' '.join(next_line_words[1:])
        text_lines[i] = text_lines[i] + " "
    text = ''
    for i in text_lines:
        text += i

def normalizacao():
    global text
    # td em minusculo
    text = text.lower()

    # acentos e especiais
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    # substitui abreviações p inteiras
    text = text.replace('fig.', 'figure')
    text = text.replace('e.g.', 'for example')
    text = text.replace('et al.', 'and others')
    text = text.replace('ch.', 'chapter')
    text = text.replace('sec.', 'section')
    text = text.replace('ref.', 'reference')
    text = text.replace('app.', 'appendix')


# realiza a limpeza dos texto
def preprocessamento():
    global text

    concatenate_word()
    
    # Remove quebra de linha
    text = re.sub(r'\n', ' ', text)
    ## essas pontuacao e numeros é importante p filtrar as secao se pa
    # text = re.sub(r'[^a-zA-Z\s]', '', text)
    # print(text)
    normalizacao()

    # Remove referencia
    references_regex = re.compile(r"References.*", re.IGNORECASE)
    text = references_regex.sub("References", text)


def identificaTermos(text):
    
    # verifica se possui as stopword
    try:
        stopwords.words('english')
    except:
        nltk.download('stopwords')
        nltk.download('punkt')
    text = re.sub(r'[^a-zA-Z\s]', '', text)
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

    # path = 'image_processing/Going_deeper_with_convolutions.pdf'
    # path = './artificial_intelligence/Deep_Residual_Learning_for_Image_Recognition.pdf'
    # path = './papers/Attributes_and_Entrepreneurial.pdf' # escrita d titulos diferente no 'text'
    path = './papers/ANALYSIS_OF_THE_IMPACT.pdf'
    # path = './papers/Internet_of_Things_Platform.pdf'
    
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

    # print(pdf_reader.pages[0])
    #print(text[:10000])
    # pattern = re.compile(r'(\n(?:ABSTRACT|\d+\. [A-Z ]+).*?)(?=\n(?:ABSTRACT|\d+\. [A-Z ]+)|\Z)', re.DOTALL)
    # matches = pattern.findall(text)
    
    re_abstract = re.compile(r'abstract([\s\S]+?(?=(1[\.]* i)))')
    # re_abstract = re.compile(r'ABSTRACT([\s\S]+?(?=INTRODUCTION|$))')
    abstract = re_abstract.findall(text)
    
    # abstract = abstract[0][1]

    print('\nAbstract:', abstract)

    re_intro = re.compile(r'introduction([\s\S]+?(?=(2[\.]* [a-z]*)))')
    intro = re_intro.findall(text)
    
    # intro = intro[0][1]
    
    print('\n\nIntroducao:', intro)

    identificaTermos(text)

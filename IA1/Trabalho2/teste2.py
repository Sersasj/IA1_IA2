# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import spacy
import PyPDF2
import re
import unicodedata
import nltk
from nltk.stem import PorterStemmer


def concatenate_word():
    global texto
    text_lines = texto.splitlines()

    for i in range(len(text_lines)):
        if len(text_lines[i]) == 0:
            continue

        if (text_lines[i][-1] == "-"):
            next_line_words = text_lines[i+1].split(" ")
            text_lines[i] = text_lines[i][:-1] + next_line_words[0] 
            text_lines[i+1] = ' '.join(next_line_words[1:])
        text_lines[i] = text_lines[i] + " "
    texto = ''
    for i in text_lines:
        texto += i

def normalizacao():
    global texto
    # td em minusculo
    texto = texto.lower()

    # acentos e especiais
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')

    # substitui abreviações p inteiras
    texto = texto.replace('fig.', 'figure')
    texto = texto.replace('e.g.', 'for example')
    texto = texto.replace('et al.', 'and others')
    texto = texto.replace('ch.', 'chapter')
    texto = texto.replace('sec.', 'section')
    texto = texto.replace('ref.', 'reference')
    texto = texto.replace('app.', 'appendix')


# realiza a limpeza dos texto
def preprocessamento():
    global texto
    
    texto = texto.replace('Methodology. ', 'Methodology ') 
    texto = texto.replace('Methodology: ', 'Methodology ') 
    texto = texto.replace('Objective. ', 'Objective ') 
    texto = texto.replace('Objective: ', 'Objective ')
    
    concatenate_word()
    
    # Remove quebra de linha
    texto = re.sub(r'\n', ' ', texto)
    # texto = re.sub(r'\.', ' ', texto)

    ## essas pontuacao e numeros é importante p filtrar as secao se pa
    texto = re.sub(r'[^a-zA-Z\s\.,]', '', texto)
    # print(texto)
    normalizacao()    
    # Remove referencia
    references_regex = re.compile(r"References.*", re.IGNORECASE)
    texto = references_regex.sub("References", texto)

    while "  " in texto:
        texto = texto.replace("  ", " ")        


# python -m spacy download pt_core_news_sm
# carrega o modelo do spacy em ingles
# python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


#path = './papers/Internet_of_Things_Platform.pdf'
path = './papers/ANALYSIS_OF_THE_IMPACT.pdf'
#path = './image_processing/Histograms_of_oriented_gradients_for_human_detection.pdf'

# Le todas a paginas do pdf
with open(path, 'rb') as pdf_file:
    # Cria obj de leitura do pdf
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    info = pdf_reader.metadata
    texto = ''
    # for i in range(len(pdf_reader.pages)):
    for i in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[i]
        texto += pdf_page.extract_text()
        # print(texto)

preprocessamento()    
# Stemming do texto
stemmer = PorterStemmer()
tokens = nltk.word_tokenize(texto)
stems = [stemmer.stem(token) for token in tokens]
stemmed_text = " ".join(stems)
stemmed_text_list= stemmed_text.split(" ")
texto_list = texto.split(" ")
texto_list = [word for word in texto_list if len(word) != 0]


# processa o texto com o spacy
doc_stem = nlp(stemmed_text)
doc = nlp(texto)
obj_bool = False
problem_bool = False
method_bool = False
contrib_bool = False

# percorre as sentenças do texto
for sent, stem_sent in zip(doc.sents, doc_stem.sents):

    # Objetivo
    if not obj_bool and ("object" not in sent.text.lower()) and ("object" in stem_sent.text.lower()) and (("studi" in stem_sent.text.lower() or "research" in stem_sent.text.lower() or "articl" in stem_sent.text.lower())):
        print("\nObjetivo:", sent)
        obj_bool = True
    elif not obj_bool and ("aim" in stem_sent.text.lower()) and (("studi" in stem_sent.text.lower() or "research" in stem_sent.text.lower() or "articl" in stem_sent.text.lower())):
        print("\nObjetivo:", sent)
        obj_bool = True    
    elif not obj_bool and ("purpose" in stem_sent.text.lower()) and (("studi" in stem_sent.text.lower() or "research" in stem_sent.text.lower() or "articl" in stem_sent.text.lower())):
        print("\nObjetivo:", sent)
        obj_bool = True      
    elif not obj_bool and ("goal" in stem_sent.text.lower()) and (("studi" in stem_sent.text.lower() or "research" in stem_sent.text.lower() or "articl" in stem_sent.text.lower())):
        print("\nObjetivo:", sent)
        obj_bool = True            
        
    # Problema
    if not problem_bool and "problem" in stem_sent.text.lower() and ("studi" in stem_sent.text.lower() 
                                                                     or "research" in stem_sent.text.lower()) and not "object" in stem_sent.text.lower():
        print("\nO problema citado no artigo é:", sent)
        problem_bool = True
    elif not problem_bool and "issue" in stem_sent.text.lower() and ("studi" in stem_sent.text.lower() 
                                                                     or "research" in stem_sent.text.lower()) and not "object" in stem_sent.text.lower():
        print("\nO problema citado no artigo é:", sent)
        problem_bool = True
    # Metodologia
    if not method_bool and "methodolog" in stem_sent.text.lower() and ("exampl" in stem_sent.text.lower() 
                                                                        or "studi" in stem_sent.text.lower() 
                                                                        or "research" in stem_sent.text.lower() 
                                                                        or "model" in stem_sent.text.lower()):
        print("\nMetodologia:", sent)
        method_bool = True

    # Contribuição
    if not contrib_bool and "contribut" in sent.text.lower():
        # imprime o contributes na tela
        print("\nContribuição:", sent)
        contrib_bool = True

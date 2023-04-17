# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

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
        
    texto = texto.replace('abstract', ' . abstract')
    texto = texto.replace('methodology. ', 'methodology ') 
    texto = texto.replace('methodology: ', 'methodology ') 
    texto = texto.replace('objective. ', 'objective ') 
    texto = texto.replace('objective: ', 'objective ')
    



#path = './papers/Internet_of_Things_Platform.pdf'
#path = './papers/ANALYSIS_OF_THE_IMPACT.pdf'
#path = './image_processing/Histograms_of_oriented_gradients_for_human_detection.pdf'
path = './papers/Learning_from_Imbalanced_Data.pdf'

def extract_info(path_pdf):
    objetivo, problema, metodologia, contribuicao = "","","",""
    global texto
    # Le todas a paginas do pdf
    with open(path_pdf, 'rb') as pdf_file:
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
    texto = " ".join(texto_list)

    

    obj_bool = False
    problem_bool = False
    method_bool = False
    contrib_bool = False
    
    sentence_list = texto.split(".")
    stem_sentence_list = stemmed_text.split(".")

    # percorre as sentenças do texto
    for sent, stem_sent in zip(sentence_list, stem_sentence_list):
   
        # Objetivo
        if not obj_bool and not ("object " in sent) and ("object " in stem_sent) and (("studi" in stem_sent or "research " in stem_sent or "articl " in stem_sent)):
            print("\nObjetivo:", sent)
            objetivo = str(sent)
            obj_bool = True
        elif not obj_bool and ("aim " in stem_sent) and (("studi " in stem_sent or "research " in stem_sent or "articl " in stem_sent)):
            print("\nObjetivo:", sent)
            objetivo = str(sent)
            obj_bool = True    
        elif not obj_bool and ("purpose " in stem_sent) and (("studi " in stem_sent or "research " in stem_sent or "articl " in stem_sent)):
            print("\nObjetivo:", sent)
            objetivo = str(sent)
            obj_bool = True      
        elif not obj_bool and ("goal " in stem_sent) and (("studi " in stem_sent or "research " in stem_sent or "articl " in stem_sent)):
            print("\nObjetivo:", sent)
            obj_bool = True       
            objetivo = str(sent)

            
        # Problema
        if not problem_bool and "problem " in stem_sent and ("studi " in stem_sent 
                                                                         or "research " in stem_sent
                                                                         or "articl " in stem_sent) and not "object" in stem_sent:
            print("\nProblema: ", sent)
            problem_bool = True
            problema = str(sent)

        elif not problem_bool and "issue " in stem_sent and ("studi " in stem_sent 
                                                                         or "research " in stem_sent
                                                                         or "articl " in stem_sent) and not "object" in stem_sent:
            print("\nnProblema: ", sent)
            problem_bool = True
            problema = str(sent)
        elif not problem_bool and "challeng " in stem_sent and ("studi " in stem_sent
                                                                          or "research " in stem_sent 
                                                                          or "articl " in stem_sent) and not "object" in stem_sent:
 
            print("\nProblema: ", sent)
            problem_bool = True
            problema = str(sent)
        # Metodologia
        if not method_bool and "methodolog " in stem_sent and ("exampl " in stem_sent 
                                                                            or "studi " in stem_sent 
                                                                            or "research " in stem_sent 
                                                                            or "model " in stem_sent):

            print("\nMetodologia:", sent)
            method_bool = True
            metodologia = str(sent)
        elif not method_bool and "conduct " in stem_sent and ("exampl " in stem_sent 
                                                                            or "studi " in stem_sent 
                                                                            or "research " in stem_sent 
                                                                            or "model " in stem_sent):

            print("\nMetodologia:", sent)
            method_bool = True
            metodologia = str(sent)
        elif not method_bool and "util " in stem_sent and ("exampl " in stem_sent 
                                                                            or "studi " in stem_sent 
                                                                            or "research " in stem_sent 
                                                                            or "model " in stem_sent):

            print("\nMetodologia:", sent)
            method_bool = True
            metodologia = str(sent)
        elif not method_bool and "employ " in stem_sent and ("exampl " in stem_sent 
                                                                            or "studi " in stem_sent 
                                                                            or "research " in stem_sent 
                                                                            or "model " in stem_sent):

            print("\nMetodologia:", sent)
            method_bool = True
            metodologia = str(sent)
            
            # Contribuição
        if not contrib_bool and "contribut " in stem_sent and ("studi " in stem_sent 
                                                                         or "research " in stem_sent
                                                                         or "articl " in stem_sent):
            # imprime o contributes na tela

            print("\nContribuição:", sent)
            contrib_bool = True
            contribuicao = str(sent)

    return objetivo, problema, metodologia, contribuicao


objetivo, problema, metodologia, contribuicao = extract_info(path)


with open('output.txt', 'w') as file:
    file.write(path.split("/")[-1]+"\n")
    file.write(objetivo + ";; " + problema + ";; " + metodologia + ";; " + contribuicao + ";;")
import os
import re
import PyPDF2
import spacy
from collections import Counter

# carrega o modelo do spacy para inglês
nlp = spacy.load("en_core_web_sm")

# lista de stopwords do spacy
stop_words = nlp.Defaults.stop_words

# leitura dos arquivos PDF
pdf_files = [f for f in os.listdir('files/') if f.endswith('.pdf')]

# criação do dicionário de termos e seus pesos
search_terms = input("Digite o termo de busca: ").lower().split()
search_terms_counter = Counter(search_terms)
search_terms_weight = {term: 1/len(search_terms_counter) for term in search_terms_counter}

# criação do dicionário de documentos e seus pesos
documents = {}
for file_name in pdf_files:
    with open('files/' + file_name, 'rb') as pdf_file:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            full_text = ''
            for page in range(len(pdf_reader.numPages)):
                page_obj = pdfReader.pages[pageNum]
                full_text += page_obj.extractText()

            # processamento do texto com spacy
            doc = nlp(full_text.lower())

            # criação do dicionário de termos do documento e seus pesos
            terms = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
            terms_counter = Counter(terms)
            max_count = max(terms_counter.values())
            terms_weight = {term: (count/max_count)*0.8 + (1-search_terms_weight.get(term, 0))*0.2
                            for term, count in terms_counter.items()}

            # cálculo do page rank
            page_rank = sum([search_terms_weight.get(term, 0)*weight for term, weight in terms_weight.items()])

            # adiciona o documento ao dicionário de documentos
            documents[file_name] = {'terms': terms_weight, 'page_rank': page_rank}

        except Exception as e:
            print(f"Could not read {file_name}. Skipping...")
            print(f"Erro: ", e)

# ordenação dos documentos por page rank
documents_sorted = sorted(documents.items(), key=lambda item: item[1]['page_rank'], reverse=True)

# exibição dos resultados
for doc, data in documents_sorted:
    print(f"{doc}: {data['page_rank']}")
    for term, weight in data['terms'].items():
        print(f"\t{term}: {weight}")
    print()

import os
import re
import operator
import argparse
import PyMuPDF


def search_files(search_term, directory):
    # lista os arquivos no diretório
    file_list = os.listdir(directory)
    # filtra apenas os arquivos com extensão .pdf
    file_list = [f for f in file_list if f.endswith('.pdf')]
    # cria um dicionário vazio para armazenar as informações do arquivo
    file_info = {}
    
    for file_name in file_list:
        try:
            # abre o arquivo usando PyMuPDF
            file_path = os.path.join(directory, file_name)
            pdf_file = PyMuPDF.open(file_path)
            # extrai o texto do arquivo
            text = ''
            for page in pdf_file:
                text += page.getText()
            # calcula o pagerank para o termo de busca
            pagerank = text.lower().count(search_term.lower())
            # armazena as informações do arquivo no dicionário
            file_info[file_name] = {
                'path': file_path,
                'pagerank': pagerank
            }
        except PyMuPDF.utils.PdfReadError:
            print(f'Could not read {file_name}. Skipping...')
    # ordena a lista de arquivos pelo pagerank em ordem decrescente
    sorted_files = sorted(file_info.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_files


def main():
    # definindo argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Search for term in PDF files.')
    parser.add_argument('term', type=str, help='Term to search in PDF files')
    parser.add_argument('--directory', '-d', type=str, default='files/', help='Directory where the PDF files are stored')
    args = parser.parse_args()

    # busca os arquivos que contêm o termo de busca
    search_results = search_files(args.term, args.directory)
    # imprime os resultados da busca
    for result in search_results:
        print(f"{result[0]} - Pagerank: {result[1]['pagerank']}")


if __name__ == '__main__':
    main()

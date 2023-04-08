import numpy as np 
import pandas as pd 

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt


def matrizDeDispersao(variaveis):
   # MATRIZ DE DISPERSAO 
   # ajuda na pre-selecao, tanto p ver quais são mais relevantes ou quais descartar pois nao tem influencia
   # para as seguintes variaveis:

   # df = pd.DataFrame(train, c = y, columns=['rooms', 'v14a', 'r4h1'])
   img = pd.plotting.scatter_matrix(X, alpha=0.5, figsize=(20, 20))
   plt.show()


if __name__ == '__main__':
    test = pd.read_csv('test.csv')
    train = pd.read_csv('train.csv')

    # Campos escolhidos para inicio da preparacao dos dados
    # Target: Objetivo => indica se a família vive ou não em pobreza extrema.
    # rooms: Número de quartos na residência (familias com pouco pode significa + pobreza)
    # idhogar: Identificador único do domicílio.
    # escolari: Anos de escolaridade da pessoa mais escolarizada no domicílio.
    # rez_esc: Anos de atraso escolar.
    # meaneduc: Média de anos de escolaridade das pessoas no domicílio.

    variaveis = ['rooms', 'idhogar', 'escolari', 
                 'rez_esc','meaneduc', 'Target']

    # X sendo os dados de treino com apenas as variaveis selecionadas
    # y sendo os resultados/classificacao de cada linha/familia
    X = train[variaveis]
    y = train['Target']

    # matrizDeDispersao(variaveis)

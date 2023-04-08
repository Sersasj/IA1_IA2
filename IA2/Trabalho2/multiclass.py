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

# Traformar em binário (dependency)


def transformar_dependente(x):
    try:
        x = float(x)
        if x <= 0.5:  # menos q 0.5 considerado nao, maior é sim
            return 0
        else:
            return 1
    except:
        if x == "no":
            return 0
        elif x == "yes":
            return 1
        else:
            return np.nan


if __name__ == '__main__':
   test = pd.read_csv('test.csv')
   train = pd.read_csv('train.csv')

   # matrizDeDispersao(variaveis)

   # Campos +importante por enquanto:
   # id: indexicacao
   # Target: Objetivo => indica se a família vive ou não em pobreza extrema.
   # Dependency: se tem ou nao dependente, pode ser binario
   # rooms: Número de quartos na residência (familias com pouco pode significa + pobreza)
   # escolari: Anos de escolaridade da pessoa mais escolarizada no domicílio.
   # meaneduc: Média de anos de escolaridade das pessoas no domicílio.

   # obs.:
   # rez_esc: Anos de atraso escolar. == muito faltante melhor remover
   # idhogar: Identificador único do domicílio == nao precisa pq ja temos o id como valores unico

   # variaveis = ['Id', 'rooms', 'escolari', 'dependency','meaneduc', 'Target']

   # todas sem as obvias reduntantes**:
   variaveis = ['Id', 'idhogar', 'hogar_nin', 'hogar_adul', 'hogar_mayor', 'hogar_total',
            'dependency', 'edjefe', 'edjefa', 'meaneduc', 'instlevel1', 'instlevel2',
            'instlevel3', 'instlevel4', 'instlevel5', 'instlevel6', 'instlevel7', 'instlevel8',
            'instlevel9', 'bedrooms', 'overcrowding', 'tipovivi1', 'tipovivi2', 'tipovivi3',
            'tipovivi4', 'tipovivi5', 'computer', 'television', 'mobilephone', 'qmobilephone',
            'lugar1', 'lugar2', 'lugar3', 'lugar4', 'lugar5', 'lugar6', 'area1', 'area2', 'age',
            'SQBescolari', 'SQBage', 'SQBhogar_total', 'SQBedjefe', 'SQBhogar_nin', 'SQBovercrowding',
            'SQBdependency', 'SQBmeaned', 'agesq', 'Target']
   
   # ====================================
   # Tratando as variaveis

   # verifica nulos, "ascending" p no notebook python fica em ordem
   print(train.isnull().sum().sort_values(ascending=False))
   print()

   # dependentes em binario
   train['dep_binario'] = train['dependency'].map(transformar_dependente)
   test['dep_binario'] = test['dependency'].map(transformar_dependente)

   # retirando valores nulos
   # print(train[['Id', 'rooms', 'escolari', 'dep_binario','meaneduc', 'Target']].isnull().sum())
   train['meaneduc'].fillna(-1, inplace=True)
   test['meaneduc'].fillna(-1, inplace=True)

   # v2a1 muitas nulas == familias que nao pagam alugueis, com isso substituimos pra 0
   train['v2a1'] = train['v2a1'].fillna(0)
   test['v2a1'] = test['v2a1'].fillna(0)

   # SQBmeaned é o quadrado da média dos valores de cada indivíduo em uma determinada casa em relação ao nível socioeconômico.
   # so 5 valor, pegamos a media
   mean_SQBmeaned = train['SQBmeaned'].mean()  # calcular a média dos valores não nulos de SQBmeaned
   train['SQBmeaned'].fillna(mean_SQBmeaned, inplace=True)
   test['SQBmeaned'].fillna(mean_SQBmeaned, inplace=True)

   # rez_esc representa o número de anos que a pessoa esteve fora da escola
   # 7928 valores faltantes ==> provavelmente nunca estiveram fora da escola
   # substituimos por 0
   train['rez_esc'].fillna(0, inplace=True)
   test['rez_esc'].fillna(0, inplace=True)

   # v18q1 se refere ao número de tablets que a família possui
   # 7342 nulos ==> substituimos por 0
   train['v18q1'].fillna(0, inplace=True)
   test['v18q1'].fillna(0, inplace=True)

   print(train.isnull().sum().sort_values(ascending=False))
   # ====================================

   # Analises!
   # EDA - Exploratory Data Analysis

   # Histograma
   
   # Target
   # Maior parte no grupo 4 = nao vulneraveis
   # sns.countplot(x='Target', data=train)
   plt.hist(train['Target'])
   plt.show()

   # Age
   # # Pico entre 15 e 25 anos, a partir disso tem uma queda gradual
   # Nossa amostra entao pode ser composta principalmente por famílias com crianças e jovens adultos.
   train['age'].hist(bins=25)
   plt.show()

   # Distribuições da variável Target por idade
   sns.displot(train, x='age', hue='Target', multiple='stack', col='Target', col_wrap=3)
   plt.show()
   # Distribuição da variável Target por escolaridade
   sns.displot(train, x='escolari', hue='Target', multiple='stack', col='Target', col_wrap=3)
   plt.show()

   # matriz de correlação para todas as variáveis
   # indica a relação entre duas variáveis
   corr_matrix = train.corr()

   # plotar a matriz de correlação usando um mapa de calor
   plt.figure(figsize=(12,8))
   sns.heatmap(corr_matrix, cmap="YlGnBu")
   plt.title("Matriz de correlação")
   plt.show()

   # Matriz de correlacao
   subset = ['v18q', 'escolari', 'age', 'tamhog', 'hogar_nin', 'Target']
   corr_matrix = train[subset].corr()
   sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
   plt.title('Correlação entre variáveis selecionadas')
   plt.show()
   # Cada célula representa a correlação entre duas variáveis, sendo que as cores indicam o valor dessa correlação, 
   # variando de -1 a 1. Quanto mais próxima do vermelho, mais forte é a correlação positiva entre as duas variáveis. 
   # Quanto mais próxima do azul, mais forte é a correlação negativa entre as duas variáveis. 
   # Já as cores amarelas e verdes indicam correlações próximas a zero.
   
   # Tamhog e hogar_nin tem uma relacao forte, isso pode indicar que elas estão relacionadas de alguma forma 
   # e que uma delas pode ser usada como um preditor da outra

   #... Testar com outras variaveis p ver se acha mais... 
   # ** Um histograma com todas nao rodou, demorou muito ae é melhor fazer separadamente


   # ====================================

   # Criação e treinamento dos modelos preditivos
   # Separacao de treino e teste (para avaliar o desempenho)
   # Pegar o "train" e fz uns % para cada, para treinar

   # X sendo os dados de treino com apenas as variaveis selecionadas
   # y sendo os resultados/classificacao de cada linha/familia
   X = train[variaveis]
   y = train['Target']

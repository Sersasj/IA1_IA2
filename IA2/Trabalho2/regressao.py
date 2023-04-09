import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC, LinearSVC
from sklearn.preprocessing import normalize
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

import seaborn as sns

def matrizDeDispersao(variaveis):
    # MATRIZ DE DISPERSAO
    # ajuda na pre-selecao, tanto p ver quais são mais relevantes ou quais descartar pois nao tem influencia
    # para as seguintes variaveis:

    # df = pd.DataFrame(train, c = y, columns=['rooms', 'v14a', 'r4h1'])
    img = pd.plotting.scatter_matrix(X, alpha=0.5, figsize=(20, 20))
    plt.show()

# Traformar em binário (dependency)

def cross_val_score_model(model, X, y, n_splits=5):
    # cv = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    cv = StratifiedKFold(n_splits=n_splits)
    scores = []
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = f1_score(y_test, y_pred, average='macro')
        scores.append(score)
    return np.mean(scores), np.std(scores)


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

## Traformar o yes e no em binário (edjefa e edjefe)
def transformar_edjef(x):
    if x == "no":
        return 0
    elif x == "yes":
        return 1
    return x
        
if __name__ == '__main__':
    test = pd.read_csv('test.csv')

    train = pd.read_csv('train.csv')
    print("Importado arquivos!\n")

    # ====================================
    # Tratando as variaveis

    print("Tratando variaveis!\n")
    # verifica nulos, "ascending" p no notebook python fica em ordem

    print("Verificando nulos:\n")
    print(train.isnull().sum().sort_values(ascending=False))
    print()

    # dependentes em binario
    train['dep_binario'] = train['dependency'].map(transformar_dependente)
    test['dep_binario'] = test['dependency'].map(transformar_dependente)

    # edjefa em binario
    train['edjefa_binario'] = train['edjefa'].map(transformar_edjef)
    test['edjefa_binario'] = test['edjefa'].map(transformar_edjef)

    # edjefe em binario
    train['edjefe_binario'] = train['edjefe'].map(transformar_edjef)
    test['edjefe_binario'] = test['edjefe'].map(transformar_edjef)

    # idhogar: Identificador único do domicílio - "fd8a6d014" ... da problema no modelo
    # pode ter +1 familia na mesma casa
    # resolver: calculamos o tamanho do domicilio com o numero de membros da familia
    # pessoas no mesmo domicilio teriam o mesmo valor
    train['tamanho_familia'] = train.groupby('idhogar')['idhogar'].transform('count')
    test['tamanho_familia'] = test.groupby('idhogar')['idhogar'].transform('count')

    # retirando valores nulos
    # print(train[['Id', 'rooms', 'escolari', 'dep_binario','meaneduc', 'Target']].isnull().sum())
    train['meaneduc'].fillna(-1, inplace=True)
    test['meaneduc'].fillna(-1, inplace=True)

    # v2a1 muitas nulas == familias que nao pagam alugueis, com isso substituimos pra 0
    train['v2a1'] = train['v2a1'].fillna(0)
    test['v2a1'] = test['v2a1'].fillna(0)

    # SQBmeaned é o quadrado da média dos valores de cada indivíduo em uma determinada casa em relação ao nível socioeconômico.
    # so 5 valor, pegamos a media
    # calcular a média dos valores não nulos de SQBmeaned
    mean_SQBmeaned = train['SQBmeaned'].mean()
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

    print("Verificando nulos:\n")
    print(train.isnull().sum().sort_values(ascending=False))
    # ====================================

    # Analises!
    # EDA - Exploratory Data Analysis

    # Histograma
    # analises()

    # ====================================

    # Campos +importante por enquanto:
    # Target: Objetivo => indica se a família vive ou não em pobreza extrema.
    # Dependency: se tem ou nao dependente, pode ser binario
    # rooms: Número de quartos na residência (familias com pouco pode significa + pobreza)
    # escolari: Anos de escolaridade da pessoa mais escolarizada no domicílio.
    # meaneduc: Média de anos de escolaridade das pessoas no domicílio.

    # obs.:
    # id: indexicacao => nao precisa usa no modelo
    # rez_esc: Anos de atraso escolar. == muito faltante melhor remover
    # idhogar: Identificador único do domicílio --- pode ter +1 familia na mesma casa => tamanho_familia
    # Uso do dep_binario em vez do dependency

    # sem as obvias reduntantes**:
    variaveis = ['tamanho_familia', 'hogar_adul', 'hogar_mayor', 'hogar_total',
                 'dep_binario', 'edjefe_binario', 'edjefa_binario', 'meaneduc', 'instlevel1', 'instlevel2',
                 'instlevel3', 'instlevel4', 'instlevel5', 'instlevel6', 'instlevel7', 'instlevel8',
                 'instlevel9', 'bedrooms', 'overcrowding', 'tipovivi1', 'tipovivi2', 'tipovivi3',
                 'tipovivi4', 'tipovivi5', 'computer', 'television', 'mobilephone', 'qmobilephone',
                 'lugar1', 'lugar2', 'lugar3', 'lugar4', 'lugar5', 'lugar6', 'area1', 'area2', 'age',
                 'SQBescolari', 'SQBage', 'SQBhogar_total', 'SQBedjefe', 'SQBhogar_nin', 'SQBovercrowding',
                 'SQBdependency', 'SQBmeaned', 'agesq']

    # Dataframes para uso no modelo
    # Dataframe X contem apenas as variaveis que desejemos como preditora (features) do modelo
    # Dataframe y contem a variavel de predicao
    X = train[variaveis]
    # Normalizar
    X = normalize(X, axis = 0, norm = 'max')
    y = train['Target']
    y = y.values
    # ====================================
    # Divisao de treino e validacao
    print("Divisao de treino e validacao!\n")

    # seed para manter a aleatoriedade *===* troca pelo random_state
    # np.random.seed(0)

    # print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    # (6689, 47) (2868, 47) (6689,) (2868,)
    
    # X Treino: 6689 exemplos de treino
    # X Validacao: 2868 exemplos de validacao
    # y treino: 6689 valor correspondente dos ex. de treino
    # y Validacao: 2868 valor correspondente dos ex. de validacao
    # ====================================
    
    # ESCOLHA 1 = Regressão Logística por ser mais simples :D
    #   - modelo linear que usa uma função logística para realizar a classificacao multiclasse
    #   - LogisticRegression

    # instancia do Modelo com parametros
    # sem o solver e até 1000 iteracao estava com retorno de aviso que nao foi convergido para um resultado otimo
    print("Criando Modelo com Regressao Linear!\n")

    # divisao 70/30 por ter um conjunto de dados "grande"
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    parametros = {
        'C'       : [.001, 0.3, .1],
        'solver'  : ['newton-cg', 'lbfgs', 'liblinear', 'saga'],
        'max_iter': [1000, 2000, 5000, 1000]
    }

    regres = LogisticRegression()

    f1 = make_scorer(f1_score , average='macro')

    clf = GridSearchCV(regres,                # modelo
                   param_grid = parametros,   # parameters
                   scoring=f1,                # metric for scoring
                   cv=3,                      # number of folds
                   verbose=1)                      

    clf.fit(X_train,y_train)

    print("Tuned Hyperparameters :", clf.best_params_ )
    print("Accuracy :", clf.best_score_)

    # print('Resuls:', clf.cv_results_)

    # # treinar utilizando tambem  oKFold (reparte em varios bloco)    
    # mean_score, std_score = cross_val_score_model(modelo, X, y, n_splits=5)
    # print(f"Mean F1 Score: {mean_score:.2f}, Std: {std_score:.2f}")

    
    # # FINAL COM O TEST.CSV
    # of_teste = test[variaveis]
    # of_teste = normalize(of_teste, axis = 0, norm = 'max')

    # p_final = modelo.predict(of_teste)
    # sub = pd.Series(p_final, index=test['Id'], name='Target')
    # sub.shape
    # sub.to_csv('subRegressao.csv', header=True)
    # print("\nArquivo subRegressao.csv criado do teste oficial!\n")
    # # Nota no kaggle com regressao linear: 0.25569
    # # Nota no kaggle da original: 0.19482

    # # vamos usar a base recomendado de avaliacao: macro F1 score
    # # Recomendado quando há múltiplas classes desbalanceadas
    # # calcula a média harmônica do F1 score de cada classe, dando o mesmo peso para todas as classes.



def analises():
    print("Realizando ANALISES!\n")
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
    sns.displot(train, x='age', hue='Target',
                multiple='stack', col='Target', col_wrap=3)
    plt.show()
    # Distribuição da variável Target por escolaridade
    sns.displot(train, x='escolari', hue='Target',
                multiple='stack', col='Target', col_wrap=3)
    plt.show()

    # matriz de correlação para todas as variáveis
    # indica a relação entre duas variáveis
    corr_matrix = train.corr()

    # plotar a matriz de correlação usando um mapa de calor
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, cmap="YlGnBu")
    plt.title("Matriz de correlação")
    plt.show()

    # matrizDeDispersao(variaveis)

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
    # "hogar_nin" representa o número de crianças (menores de 19 anos) no mesmo domicílio.
    # "tamhog" representa o tamanho total do domicílio (número total de pessoas que vivem no mesmo domicílio).
    # Chutamos q tamhog sera mais relevante, por analisarmos a pobreza em conjunto da familia

    # ... Testar com outras variaveis p ver se acha mais...
    # ** Um histograma com todas nao rodou, demorou muito ae é melhor fazer separadamente

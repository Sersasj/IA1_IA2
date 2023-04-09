##  Tecnicas de machine learning em Previsão da pobreza doméstica na Costa Rica

* Trabalho 2
* Alunos:
  - Gabriel Thiago -  RA: 107774
  - Sergio Alvarez  -  RA: 115735 

* Disciplina: 
  * Aprend. Maq. e Model. Conhec. Incerto.

----------------

#### Files 

- Técnica 1 - Logistic Regression
  - [regressao.py](./regressao.py)
- Técanica 2 - Random Forest
  - [random_forest.py](./random_forest.py)
- Pacotes necessários
  - [requirements.txt](./requirements.txt)
- All Data fields - Variable name, Variable description
  - [codebook.csv](./codebook.csv)
- Dataset teste - sem 'Target'
  - [test.csv](./test.csv)
- Dataset treino - com 'Target'
  - [train.csv](./train.csv)

----------------
### Sobre o problema

- Site extraido o notebook python: https://www.kaggle.com/competitions/costa-rican-household-poverty-prediction/data

- Introdução sobre o problema: https://www.kaggle.com/code/willkoehrsen/a-complete-introduction-and-walkthrough

- Tecnica sample submission - Score: 0.19482
- Tecnicas utilizadas de acordo com a Intro (2 linha acima):
  - Support Vector Classifier (Linear SVC) = 10 Fold CV Score: 0.28346 with std: 0.04484
  - Gaussian Naive Bayes (GaussianNB) = 10 Fold CV Score: 0.17935 with std: 0.03867
  - Multi-layer Perceptron classifier (MLPClassifier) = 10 Fold CV Score: 0.28674 with std: 0.06301
  - Linear Discriminant Analysis (LDA) = 10 Fold CV Score: 0.32217 with std: 0.05984
  - Ridge Classifier CrossValidation = 10 Fold CV Score: 0.27896 with std: 0.03675
  - KNN
    - KNN with 5 neighbors = 10 Fold CV Score: 0.35078 with std: 0.03829
    - KNN with 10 neighbors = 10 Fold CV Score: 0.32153 with std: 0.03028
    - KNN with 20 neighbors = 10 Fold CV Score: 0.31039 with std: 0.04974
  - Extra-trees classifier = 10 Fold CV Score: 0.32215 with std: 0.04671


----------------

### Descrição dataset

Os dados desta competição são disponibilizados em dois arquivos: train.csv e test.csv. 
O conjunto de treinamento possui 9.557 linhas e 143 colunas, enquanto o conjunto de teste possui 23.856 linhas e 142 colunas. 
Cada linha representa um indivíduo e cada coluna é uma característica, seja exclusiva do indivíduo ou da família do indivíduo. 
O conjunto de treinamento tem uma coluna adicional, target, que representa o nível de pobreza em uma escala de 1 a 4 e é o rótulo da competição. Um valor de 1 é a pobreza mais extrema.

Este é um problema de aprendizado de máquina de classificação multiclasse supervisionado:

- Supervisionado: fornecido com os rótulos para os dados de treinamento
- Classificação multiclasse: rótulos são valores discretos com 4 classes

#### {train|test}.csv - the training set
- Train (with a Target column)
- Test (without the Target column).

- One row represents one person in our data sample.
- Multiple people can be part of a single household. Only predictions for heads of household are scored.

#### sample_submission.csv - a sample submission file in the correct format
- This file contains all test IDs and a default value.
- Note that ONLY the heads of household are used in scoring. All household members are included in test + the sample submission, but only heads of households are scored.


#### Core Data fields

- Id - a unique identifier for each row.
- Target - the target is an ordinal variable indicating groups of income levels.
  - 1 = extreme poverty           / pobreza extrema
  - 2 = moderate poverty          / pobreza moderada
  - 3 = vulnerable households     / familias vulneraveis
  - 4 = non vulnerable households / familias nao vulneraveis

- idhogar - this is a unique identifier for each household. This can be used to create household-wide features, etc. All rows in a given household will have a matching value for this identifier.
- parentesco1 - indicates if this person is the head of the household.
- This data contains 142 total columns.


### Objetivo
O objetivo é prever a pobreza no nível familiar. 
Recebemos dados no nível individual, com cada indivíduo tendo características únicas, mas também informações sobre sua família. 
Para criar um conjunto de dados para a tarefa, teremos que realizar algumas agregações dos dados individuais de cada domicílio. Além disso, temos que fazer uma previsão para cada indivíduo no conjunto de teste, mas "APENAS os chefes de família são usados na pontuação", o que significa que queremos prever a pobreza com base na família.

#### Probleminha
Quando criamos um modelo, treinamos com base na família com o rótulo para cada família, o nível de pobreza do chefe da família. Os dados brutos contêm uma mistura de características familiares e individuais e, para os dados individuais, teremos que encontrar uma maneira de agregar isso para cada família. Alguns dos indivíduos pertencem a uma família sem chefe de família, o que significa que, infelizmente, não podemos usar esses dados para treinamento. Esses problemas com os dados são completamente típicos dos dados do mundo real e, portanto, esse problema é uma ótima preparação para os conjuntos de dados que você encontrará em um trabalho de ciência de dados!

### Mètrica
Por fim, queremos construir um modelo de aprendizado de máquina que possa prever o nível inteiro de pobreza de uma família. Nossas previsões serão avaliadas pelo Macro F1 Score. Você pode estar familiarizado com a pontuação F1 padrão para problemas de classificação binária, que é a média harmônica de precisão e recuperação:

$$F_1 = \frac{2}{\tfrac{1}{\mathrm{recall}} + \tfrac{1}{\mathrm{precision}}} = 2 \cdot \frac{\mathrm{precision} \cdot \mathrm{recall}}{\mathrm{precision} + \mathrm{recall}}$$

Para problemas multi-classe, temos que calcular a média das pontuações F1 para cada classe. A pontuação F1 macro calcula a média da pontuação F1 para cada classe sem levar em consideração os desequilíbrios de rótulos.

$$\text{Macro F1} = \frac{\text{F1 Class 1} + \text{F1 Class 2} + \text{F1 Class 3} + \text{F1 Class 4}}{4}$$


Em outras palavras, o número de ocorrências de cada rótulo não entra no cálculo ao usar a macro (ao contrário do que acontece ao usar a pontuação "ponderada"). (Para obter mais informações sobre as diferenças, consulte a [Documentação do Scikit-Learn para F1 Score] ou esta [perguntas e respostas do Stack Exchange]. 
Se quisermos avaliar nosso desempenho, podemos usar o código:

```
from sklearn.metrics import f1_score
f1_score(y_true, y_predicted, average = 'macro`)
```

Para esse problema, os rótulos estão desequilibrados, o que torna um pouco estranho usar a média macro para a métrica de avaliação, mas essa é uma decisão tomada pelos organizadores e não algo que possamos mudar! Em seu próprio trabalho, você deseja estar ciente dos desequilíbrios de rótulos e escolher uma métrica de acordo.
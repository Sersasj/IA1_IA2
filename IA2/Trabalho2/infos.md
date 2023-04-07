- Site extraido o notebook python: https://www.kaggle.com/competitions/costa-rican-household-poverty-prediction/data

- Introdução sobre o problema: https://www.kaggle.com/code/willkoehrsen/a-complete-introduction-and-walkthrough

- Tenica originalmente utilizada (Técnica A):

----------------

### Descrição dataset

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


----------------

#### Files 

- [codebook.csv](./codebook.csv) => All Data fields - Variable name, Variable description
- [test.csv](./test.csv) => dataset teste - sem target
- [train.csv](./train.csv) => dataset treino - com target

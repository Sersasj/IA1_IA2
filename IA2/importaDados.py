import os
import pandas as pd

# caminho para dataset (windows/linux)
data_path = os.path.join(os.path.dirname(__file__), "dataset", "brasileirao.csv")

# Importa base de dados
df = pd.read_csv(data_path)

print(df)

totalLinha = len(df)
print(totalLinha)
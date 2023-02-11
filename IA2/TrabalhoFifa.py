import pandas as pd
from natsort import natsort_keygen
import csv
from unidecode import unidecode
import unicodedata

# Carrega dados dos anos 2019, 2020 e 2021
df_brasileirao = pd.read_csv('dataset/brasileirao.csv')
df_brasileirao = df_brasileirao[df_brasileirao['year'].isin([2019,2020,2021])]
# Muda coluna do nome
df_brasileirao.rename(columns={'team': 'club_name'}, inplace=True)

# Muda nome dos times
df_brasileirao.rename(columns={'team': 'club_name'}, inplace=True)


# Nome dos times que estavam no brasileirão 
times_brasileirao = df_brasileirao['club_name'].tolist()
times_brasileirao = list(set(times_brasileirao))

# Carrega dados para df
df1 = pd.read_csv("dataset_fifa/players_19.csv")
df2 = pd.read_csv("dataset_fifa/players_20.csv")
df3 = pd.read_csv("dataset_fifa/players_21.csv")
df_players = pd.concat([df1,df2,df3])


df_players = df_players[df_players["club_name"].isin(times_brasileirao)]
# Pega infos que queremos
df_players = df_players[['club_name', 'overall', 'age', 'pace', 'shooting', 'passing', 'defending']]
# Substitui nan pela média
df_players.fillna(df_players.mean(numeric_only=True), inplace=True)


# Exclui times que não temos info
clubes = df_players['club_name'].tolist()
clubes = list(set(clubes))
df_brasileirao = df_brasileirao[df_brasileirao['club_name'].isin(clubes)]


# Discretiza informações
df_brasileirao["category"] = "neutro"
df_brasileirao.loc[df_brasileirao["position"] <= 4, "category"] = "G4"
df_brasileirao.loc[df_brasileirao["position"] >= 16, "category"] = "rebaixado"


# Junta tabela dos times e dos jogadores
merged_df = pd.merge(df_players, df_brasileirao, on='club_name', how='inner')
mean_table = merged_df.groupby(["category"]).mean(numeric_only='True')

##########

def calculate_utility(mean_table, entry_table):
    print("aa")
    #(overall_G4 - overall_time) / overall_G4


##############
# Simulação
df_brasileirao_sim = pd.read_csv('dataset/brasileirao.csv')
df_brasileirao_sim = df_brasileirao_sim[df_brasileirao_sim['year'] == 2022]
df_brasileirao_sim.rename(columns={'team': 'club_name'}, inplace=True)

simulation_df = pd.read_csv("dataset_fifa/players_22.csv", low_memory=False)
df_players_palmeiras = simulation_df[simulation_df["club_name"] == 'Palmeiras']
df_players_palmeiras = df_players_palmeiras[['club_name', 'overall', 'age', 'pace', 'shooting', 'passing', 'defending']]
df_players_palmeiras.fillna(df_players_palmeiras.mean(numeric_only=True), inplace=True)
df_players_palmeiras_mean = df_players_palmeiras.groupby(["club_name"]).mean(numeric_only='True')

calculate_utility(mean_table, df_players_palmeiras_mean)

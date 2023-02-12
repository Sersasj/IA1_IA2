import pandas as pd
from natsort import natsort_keygen
import csv
from unidecode import unidecode
import unicodedata
import numpy as np
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

def calculate_utility(club_name, mean_table, team_table):

    # Define the probability tables for each variable
    overall_probs = np.array(mean_table['overall'].tolist())/100
    pace_probs = np.array(mean_table['pace'].tolist())/100
    shooting_probs = np.array(mean_table['shooting'].tolist())/100
    passing_probs = np.array(mean_table['passing'].tolist())/100
    defending_probs = np.array(mean_table['defending'].tolist())/100
    
    overall_team = np.array(team_table['overall'].tolist())/100
    pace_team = np.array(team_table['pace'].tolist())/100
    shooting_team = np.array(team_table['shooting'].tolist())/100
    passing_team = np.array(team_table['passing'].tolist())/100
    defending_team = np.array(team_table['defending'].tolist())/100 
    

    probs = np.zeros(3)
    for i in range(3):
        overall = 1 - abs((overall_probs[i] - overall_team)) / overall_probs[i] 
        pace = 1 - abs((pace_probs[i] - pace_team))/ pace_probs[i] 
        shooting = 1 - abs((shooting_probs[i] - shooting_team)) / shooting_probs[i] 
        passing = 1 - ((passing_probs[i] - passing_team)) / passing_probs[i] 
        defending = 1 - abs((defending_probs[i] - defending_team)) / defending_probs[i] 
        probs[i] = overall + pace + shooting + passing + defending
        
        
    team_position = np.argmax(probs)

    if team_position == 0:        
        print("O {} terminará o campeonato no G4".format(club_name))
    elif team_position == 1:        
        print("O {} terminará o campeonato neutro".format(club_name))
    else:
        print("O {} terminará o campeonato na zona de rebaixamento".format(club_name))
        
    print("Função utilidade: ",probs)  
##############
# Simulação palmeiras
df_brasileirao_sim = pd.read_csv('dataset/brasileirao.csv')
df_brasileirao_sim = df_brasileirao_sim[df_brasileirao_sim['year'] == 2022]
df_brasileirao_sim.rename(columns={'team': 'club_name'}, inplace=True)

simulation_df = pd.read_csv("dataset_fifa/players_22.csv", low_memory=False)
df_players_sim = simulation_df[simulation_df["club_name"] == 'Palmeiras']
df_players_sim = df_players_sim[['club_name', 'overall', 'age', 'pace', 'shooting', 'passing', 'defending']]
df_players_sim.fillna(df_players_sim.mean(numeric_only=True), inplace=True)
df_players_sim_mean = df_players_sim.groupby(["club_name"]).mean(numeric_only='True')
calculate_utility('Palmeiras', mean_table, df_players_sim_mean)


# Simulação Botafogo
df_brasileirao_sim = pd.read_csv('dataset/brasileirao.csv')
df_brasileirao_sim = df_brasileirao_sim[df_brasileirao_sim['year'] == 2022]
df_brasileirao_sim.rename(columns={'team': 'club_name'}, inplace=True)

simulation_df = pd.read_csv("dataset_fifa/players_22.csv", low_memory=False)
df_players_sim = simulation_df[simulation_df["club_name"] == 'Santos']
df_players_sim = df_players_sim[['club_name', 'overall', 'age', 'pace', 'shooting', 'passing', 'defending']]
df_players_sim.fillna(df_players_sim.mean(numeric_only=True), inplace=True)
df_players_sim_mean = df_players_sim.groupby(["club_name"]).mean(numeric_only='True')
calculate_utility('Goiás', mean_table, df_players_sim_mean)

# Simulação Atlético Clube Goianiense
df_brasileirao_sim = pd.read_csv('dataset/brasileirao.csv')
df_brasileirao_sim = df_brasileirao_sim[df_brasileirao_sim['year'] == 2022]
df_brasileirao_sim.rename(columns={'team': 'club_name'}, inplace=True)

simulation_df = pd.read_csv("dataset_fifa/players_22.csv", low_memory=False)
df_players_sim = simulation_df[simulation_df["club_name"] == 'Atlético Clube Goianiense']
df_players_sim = df_players_sim[['club_name', 'overall', 'age', 'pace', 'shooting', 'passing', 'defending']]
df_players_sim.fillna(df_players_sim.mean(numeric_only=True), inplace=True)
df_players_sim_mean = df_players_sim.groupby(["club_name"]).mean(numeric_only='True')
calculate_utility('Atlético Clube Goianiense', mean_table, df_players_sim_mean)

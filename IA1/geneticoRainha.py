# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:34:22 2023

@author: sergi
"""
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import sys
def create_chromosome(number_of_queens):
    """
    Cria um cromossomo aleatório com as possíveis posições das damas
    não existe posição repetida
    Parâmetros:
    number_of_queens -- quantidade de damas no tabuleiro 
    Retorna:
    np.array de tamanho [1, ..., number_of_queens] 
    """
    chromosome = np.arange(number_of_queens)
    np.random.shuffle(chromosome)
    return chromosome    
    

def fitness(chromosome):
    """
    Calcula o fitness do cromossomo
    o fitness é calculado pelo numero de pares de rainhas (i, j), i < j que não se atacam
    o maximo de fitness é um somatório de 1 até (numRainhas - 1)
    ex: em um tabuleiro 8X8 o fitness maximo é 28
    Parâmetros:
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    Retorna:
    inteiro com a fitness do cromossomo.
    """
    fitness = 0
    for i in range(len(chromosome)):
        for j in range(i+1, len(chromosome)):
            # horizontal
            if chromosome[i] == chromosome[j]:
                continue
            # diagonal
            if j-i == abs(chromosome[i] - chromosome[j]):
                continue
            fitness += 1
    return fitness    

def probability(chromosome):
    """
    Calcula a probabilidade de escolha dos pais
    quanto mais perto do max fitness maior a probabilidade
    Parâmetros:    
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    Retorna:
    probabilidade de escolha dos pais
    """
    number_of_queens = len(chromosome)
    max_fitness = (number_of_queens*(number_of_queens-1))/2 
    return fitness(chromosome) / max_fitness



def roulette_selection(probabilities):
    """
    Seleciona um cromossomo da população
    a escolha é feita com base no fitness de cada cromossomo
    Parâmetros:
    population -- lista com probabilidades
    Retorna:
    index do cromossomo selecionado
    """    
    # Calculate the cumulative probabilities
    cum_probs = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    
    # Generate a random number between 0 and 1
    rand = random.uniform(0, cum_probs[-1])    
    # Find the index corresponding to the random number
    for i, cum_prob in enumerate(cum_probs):
        if rand < cum_prob:
            return i


def reproduce(parent1, parent2):
    """
    Faz o cruzamento entre dois cromossomos
    faz o crossover em um ponto do cromossomo
    obx crossover
    Parâmetros:    
    chromosome1 :  cromossomo pai
    chromosome2 :  cromossomo mae
    Retorna:
    cromossomos filho    
    """
    # select a random subset of values from parent 1
    subset = set(np.random.choice(parent1, len(parent1) // 2, replace=False))
    # initialize offspring with subset from parent 1
    offspring = np.array([val if val in subset else None for val in parent1])
    # fill remaining positions in offspring with values from parent 2
    i = 0
    for val in parent2:
        if val not in subset:
            while offspring[i] is not None:
                i += 1
            offspring[i] = val
    return offspring

def mutate(chromosome):
    """
    Muta um cromossomo
    a mutação troca a posição de duas damas no cromossomo 
    Parâmetros:
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    Retorna:
    cromossomo mutado
    """
  
    idx1, idx2 = random.sample(range(len(chromosome)), 2)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

def epochs(population, mutation_probability, population_size, probabilities):
    """
    Realiza o cruzamento, adiciona na nova população 
    Parâmetros:
    population -- np.array com cromossomos
    mutation_probability -- probabilidade de ocorrencia de uma mutação
    Retorna:
    nova população
    """
    for i in range(population_size // 2):
        parent_chromosome_1_idx = (roulette_selection(probabilities))
        parent_chromosome_2_idx = (roulette_selection(probabilities))
        parent_chromosome_1 = population[parent_chromosome_1_idx]
        parent_chromosome_2 = population[parent_chromosome_2_idx]

        offspring_chromosome_1 = reproduce(parent_chromosome_1, parent_chromosome_2)
        offspring_chromosome_2 = reproduce(parent_chromosome_1, parent_chromosome_2)

        if random.random() < mutation_probability:
            offspring_chromosome_1 = mutate(offspring_chromosome_1)
        if random.random() < mutation_probability:
            offspring_chromosome_2 = mutate(offspring_chromosome_2)

        #elitism
        new_population = np.stack((parent_chromosome_1, parent_chromosome_2, 
                                   offspring_chromosome_1, offspring_chromosome_2))
        fitness_values = np.apply_along_axis(fitness, 1, new_population)

        sorted_indices = np.argsort(fitness_values)[::-1]
        population[[parent_chromosome_1_idx, parent_chromosome_2_idx]] = new_population[sorted_indices[:2]]
            
    return population  

def solution(population, max_fitness):
    """
    Seleciona o cromossomo com uma solução do n-rainhas
    Parâmetros:
    population -- lista com cromossomos
    max_fitness -- inteiro com o valor maximo do fitness
    Retorna:
    Cromossomo com uma solução do n-rainhas
    """
    for chromosome in population:
        if fitness(chromosome) == max_fitness:
            return chromosome
    print("Solução não encontrada")
    
def show_chromosome(chromosome):
    """
    Printa informações do cromossomo
    Parâmetros:
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    Retorna:
    None
    """
    print("Cromossomo = {},  Fitness = {}".format(str(chromosome),
                                                  fitness(chromosome)))
    
def show_board(chromosome, number_of_queens):
    """
    Printa o tabuleiro com a solução de um cromossomo
    Parâmetros:
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    number_of_queens -- inteiro com a qnt de damas
    Retorna:
    None.
    """
    board = np.full((number_of_queens, number_of_queens), "x")
    
    for i in range(number_of_queens):
        board[int(chromosome[i]), i] = "Q" 
        
    for row in board:
        print (" ".join(row))
        
def time_test():
    """
    Testa o tempo médio de execução para o problema de n-rainhas de 4...22
    Plota um gráfico com o tempo médio
    Retorna:
    None  
    """
    # [0.001214039999993588, 0.0015303299999999353, 0.011732140000000868, 0.027880650000000173, 0.06255439999999908, 0.09307983999999862, 0.22705601000000114, 0.6774491000000011, 1.6124172499999987, 2.0004818399999977, 3.544387699999993, 8.044407640000008, 8.045281700000004, 18.34614865000002, 36.09995972, 50.40309513000004, 68.59274187000003, 102.83478264000007]
    
    population_size = 100
    result = [] 
    
    for number_of_queens in range(4,22):   
        time_list = []
        for i in range(10):
            start = time.perf_counter()
            numbers_of_generations = 1
            mutation_probability = 0.1
            max_fitness = (number_of_queens*(number_of_queens-1))/2  
            population = np.zeros((population_size,number_of_queens))
            for i in range(len(population)):
                population[i] = create_chromosome(number_of_queens)   
            probabilities = [probability(chromosome) for chromosome in population]
            while not 1 in probabilities:              
                population = epochs(population, mutation_probability, population_size, probabilities)    
                probabilities = [probability(chromosome) for chromosome in population]
                numbers_of_generations += 1
            end = time.perf_counter()
            time_list.append(end-start)
            print(time_list)
        result.append(np.mean(time_list))
    print(result)
    

    X = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

    Y = result
    plt.xticks(range(min(X), max(X)+1))

    plt.plot(X, Y, label = "genético")    
    plt.title("Tempo de execução - Genético")    
    plt.xlabel("Número de damas")
    plt.ylabel("Tempo (em segundos)")
    plt.savefig("time_of_execution_genetic.png",dpi=400)

def main():  
    
    #time_test()
    
    print("---------------------------------------")
    print("| Selecione a complexidade do problema|")
    print("| 1 - Complexidade baixa - 10 damas    |")
    print("| 2 - Complexidade média - 14 damas   |")
    print("| 3 - Complexidade alta - 20 damas    |")
    print("---------------------------------------")
    selection = int(input("Digite sua opção: "))
    if selection == 1:
        number_of_queens = 10
    elif selection == 2:
        number_of_queens = 14
    elif selection == 3:
        number_of_queens = 20
    else:
        print("Opção inválida")
        sys.exit()

    population_size = 100
    mutation_probability = 0.4
    population = np.zeros((population_size,number_of_queens))
    max_fitness = (number_of_queens*(number_of_queens-1))/2    
    numbers_of_generations = 1


    for i in range(len(population)):
        population[i] = create_chromosome(number_of_queens)   
    probabilities = [probability(chromosome) for chromosome in population]
    while not 1 in probabilities: 
        population = epochs(population, mutation_probability, population_size, probabilities)    
        best_chromossome = probabilities.index(max(probabilities))
        print("Cromossomo com maior fitness maxima atual: ")
        show_chromosome(population[best_chromossome])
        probabilities = [probability(chromosome) for chromosome in population]
    
    print("Solução encontrada na geração {}".format(numbers_of_generations))
    possible_solution = solution(population, max_fitness)
    print("Uma solução possível para o problema de {}-damas é {}".format(number_of_queens,
                                                                         possible_solution))
    show_board(possible_solution, number_of_queens)
    
if __name__ == "__main__":
    main()
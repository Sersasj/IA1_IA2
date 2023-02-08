# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:19:19 2023

@author: sergi
"""
import time
import random
import numpy as np
import sys
import matplotlib.pyplot as plt

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

def has_repeating_numbers(array):
    """
    Verifica se um array tem elementos repetidos
    Parâmetros:    
    array -- np.array
    Retorna:
    True se existe um elemento repetido
    False se não
    """
    unique_elements, counts = np.unique(array, return_counts=True)
    return np.any(counts > 1)

def reproduce(parent_chromosome_1, parent_chromosome_2):
    """
    Faz o cruzamento entre dois cromossomos
    faz o crossover em um ponto do cromossomo
    caso o cruzamento seja invalido ele é refeito
    Parâmetros:    
    chromosome1 :  cromossomo pai
    chromosome2 :  cromossomo mae
    Retorna:
    cromossomos filho    
    """
    crossover_point = random.randint(0, len(parent_chromosome_1)-1)
    offspring_chromosome_1 = np.concatenate((parent_chromosome_1[:crossover_point], parent_chromosome_2[crossover_point:]))
    offspring_chromosome_2 = np.concatenate((parent_chromosome_2[:crossover_point], parent_chromosome_1[crossover_point:]))
    while (has_repeating_numbers(offspring_chromosome_2) and has_repeating_numbers(offspring_chromosome_2)): 
        crossover_point = random.randint(0, len(parent_chromosome_1)-1)
        offspring_chromosome_1 = np.concatenate((parent_chromosome_1[:crossover_point], parent_chromosome_2[crossover_point:]))
        offspring_chromosome_2 = np.concatenate((parent_chromosome_2[:crossover_point], parent_chromosome_1[crossover_point:]))

    return offspring_chromosome_1, offspring_chromosome_2

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

def roullete_pick(population):
    """
    Seleciona um cromossomo da população
    a escolha é feita com base no fitness de cada cromossomo
    Parâmetros:
    population -- lista com cromossomos
    Retorna:
    index do cromossomo selecionado
    """    
    probabilities = [probability(chromosome) for chromosome in population]
    # normaliza probabilidades
    total = sum(probabilities)
    probabilities = [prob/total for prob in probabilities]
    idx = np.random.choice(len(population), 1, p=probabilities)
    return idx[0]


   
def epochs(population, mutation_probability):
    """
    Realiza o cruzamento, adiciona na nova população 
    Parâmetros:
    population -- lista com cromossomos
    mutation_probability -- probabilidade de ocorrencia de uma mutação
    Retorna:
    nova população
    """
    new_population = []
    for i in range(len(population) // 2):
        parent_chromosome_1 = population[roullete_pick(population)]
        parent_chromosome_2 = population[roullete_pick(population)]
        offspring_chromosome_1, offspring_chromosome_2 = reproduce(parent_chromosome_1,
                                                                   parent_chromosome_2)
        if random.random() < mutation_probability:
            offspring_chromosome_1 = mutate(offspring_chromosome_1)
        if random.random() < mutation_probability:
            offspring_chromosome_2 = mutate(offspring_chromosome_2)            
        new_population.append(offspring_chromosome_1)        
        new_population.append(offspring_chromosome_2)
    return new_population        


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
    
def time_test():
    """
    Testa o tempo médio de execução para o problema de n-rainhas de 4...10
    Plota um gráfico com o tempo médio
    Retorna:
    None
    """
    # Resultado
    Y1 = [0.0011059000001296226, 0.001464750000013737, 1.4886926599999242, 0.9575531100000717, 9.563682670000025, 17.365219170000092, 79.44766261000004, 263.24039344]
    population_size = 100
    result = []
    """
    for number_of_queens in range(4,12):   
        time_list = []
        for i in range(10):
            start = time.perf_counter()
            numbers_of_generations = 1
            mutation_probability = 0.1
            max_fitness = (number_of_queens*(number_of_queens-1))/2     
            population = [create_chromosome(number_of_queens) for i in range(population_size)]    
            while not max_fitness in [fitness(chromosome) for chromosome in population]:
                population = epochs(population, mutation_probability)    
                fitness_list = [fitness(chromosome) for chromosome in population]
                numbers_of_generations += 1
    
            end = time.perf_counter()
            time_list.append(end-start)
            print(time_list)
        result.append(np.mean(time_list))
    print(result)
    """
    X1= [4, 5, 6, 7, 8, 9, 10, 11]
    X2 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    Y2 = [0.001334849999994958, 0.0010872799999987136, 0.0188632699999971, 0.03865948000000401, 0.10604329999999607, 0.3117452799999995, 3.8193840500000023, 9.175329600000003, 37.35564776, 34.212411299999985, 304.13998848999995]

    #Y = result
    plt.xticks(range(min(X2), max(X2)+1))

    plt.plot(X1, Y1, label = "genético")    
    plt.plot(X2, Y2, label = "tabu")    
    
    plt.legend()
    plt.title("Tempo de execução - Comparação")    
    plt.xlabel("Número de damas")
    plt.ylabel("Tempo (em segundos)")
    plt.savefig("time_of_execution_comparition.png",dpi=400)

    
def show_board(chromosome, number_of_queens):
    """
    Printa o tabuleiro com a solução de um cromossomo
    Parâmetros:
    chromosome -- np.array com a posição de cada rainha no tabuleiro
    number_of_queens -- inteiro com a qnt de damas
    Retorna:
    None.
    """
    board = []
    
    for x in range(number_of_queens):
        board.append(["x"] * number_of_queens)
        
    for i in range(number_of_queens):
        board[chromosome[i]][i]="Q" 
        
    for row in board:
        print (" ".join(row))  

def main():  
    
    time_test()
    """
    print("---------------------------------------")
    print("| Selecione a complexidade do problema|")
    print("| 1 - Complexidade baixa - 6 damas    |")
    print("| 2 - Complexidade média - 8 damas   |")
    print("| 3 - Complexidade alta - 10 damas    |")
    print("---------------------------------------")
    selection = int(input("Digite sua opção: "))
    if selection == 1:
        number_of_queens = 6
    elif selection == 2:
        number_of_queens = 8
    elif selection == 3:
        number_of_queens = 10
    else:
        print("Opção inválida")
        sys.exit()

    population_size = 100
    mutation_probability = 0.1
    max_fitness = (number_of_queens*(number_of_queens-1))/2     
    population = [create_chromosome(number_of_queens) for i in range(population_size)]    
    numbers_of_generations = 1

    while not max_fitness in [fitness(chromosome) for chromosome in population]:
        print("----- Geração {} -----".format(numbers_of_generations))
        print("")
        population = epochs(population, mutation_probability)    
        fitness_list = [fitness(chromosome) for chromosome in population]
        best_chromossome = fitness_list.index(max(fitness_list))
        
        print("Cromossomo com maior fitness maxima atual: ")
        show_chromosome(population[best_chromossome])
        print("Fitness média ", np.mean(fitness_list))
        numbers_of_generations += 1
        #if numbers_of_generations > 1000:
        #    break
    
    print("Solução encontrada na geração {}".format(numbers_of_generations))
    possible_solution = solution(population, max_fitness)
    print("Uma solução possível para o problema de {}-damas é {}".format(number_of_queens,
                                                                         possible_solution))
    show_board(possible_solution, number_of_queens)
    """
if __name__ == "__main__":
    main()
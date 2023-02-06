# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:19:19 2023

@author: sergi
"""

import random
import numpy as np

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

def reporoduce(parent_chromosome_1, parent_chromosome_2):
    """
    Faz o cruzamento entre dois cromossomos
    faz o crossover em dois pontos do cromossomo
    ---------permite cruzamentos falhos -- talvez mudar depois-------------
    Parâmetros:    
    chromosome1 :  cromossomo pai
    chromosome2 :  cromossomo mae
    Retorna:
    cromossomos filho
    """
    idx1, idx2 = random.sample(range(len(parent_chromosome_1)), 2)
    offspring_chromosome_1 = np.concatenate((parent_chromosome_1[:idx1],
                                             parent_chromosome_2[idx1:idx2], 
                                             parent_chromosome_1[idx2:]))
    
    offspring_chromosome_2 = np.concatenate((parent_chromosome_2[:idx1], 
                                             parent_chromosome_1[idx1:idx2],
                                             parent_chromosome_2[idx2:]))
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
    probabilities = [probability(chromosome) for chromosome in population]
    # normaliza probabilidades
    total = sum(probabilities)
    probabilities = [prob/total for prob in probabilities]
    idx = np.random.choice(len(population), 1, p=probabilities)
    print(idx)
    """
    """
    
def main():
    """
    Step 1: A random chromosome is generated
    Step 2: Fitness value of the chromosome is calculated
    Step 3: If fitness is not equal to Fmax
    Step 4: Reproduce (crossover) new chromosome from 2 randomly selected best chromosomes
    Step 5: Mutation may take place
    Step 6: New chromosome added to population
    Repeat Step 2 to 6 until a chromosome (solution) with Fitness value = Fmax is found
    """
    
    """
    number_of_queens = 8
    population_size = 100
    max_fitness = (number_of_queens*(number_of_queens-1))/2 
    
    population = [create_chromosome(number_of_queens) for i in range(population_size)]
    
    while not max_fitness in [fitness(chromosome) for chromosome in population]:
    """
        
    x = create_chromosome(8)
    y = create_chromosome(8)
    #x = mutate(x)
    roullete_pick([x,y])
    filho1, filho2 = reporoduce(x,y)

if __name__ == "__main__":
    main()
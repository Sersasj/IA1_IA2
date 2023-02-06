# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:02:47 2023

@author: sergi

"""
import numpy as np
import random
import math


def total_conflicts(board):
    """
    Calcula a quantidade de conflitos do tabuleiro fitness do cromossomo
    Parâmetros:
    board -- np.array com a posição de cada rainha no tabuleiro
    Retorna:
    inteiro com a quantidade de conflitos do tabuleiro.
    """
    conflicts = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            # horizontal
            if board[i] == board[j]:
                conflicts += 1
            # diagonal
            if j-i == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts    


def generate_board(number_of_queens):
    """
    Cria um cromossomo aleatório com as possíveis posições das damas
    não existe posição repetida
    Parâmetros:
    number_of_queens -- quantidade de damas no tabuleiro 
    Retorna:
    np.array de tamanho [1, ..., number_of_queens] 
    """
    board = np.arange(number_of_queens)
    np.random.shuffle(board)
    return board    

def tabu_search(number_of_queens, tabu_list_size=100):
    """
    Realiza a busca tabu
    Parâmetros:
    number_of_queens -- quantidade de damas no tabuleiro 
    tabu_list_size -- tamanho da lista tabu
    Retorna:
    solução encontrada

    """
    board = generate_board(number_of_queens)
    best = board[:]
    best_conflicts = total_conflicts(best)
    tabu_list = []
    while best_conflicts != 0:
        print(best_conflicts)  
        row, column = random.sample(range(number_of_queens), 2) 
        current = best[row]
        best[row] = column
        current_conflicts = total_conflicts(best)
        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            tabu_list.append(best[:])
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
        else:
            best[row] = current
        neighbors = [(row, c) for c in range(number_of_queens) if c != current]
        random.shuffle(neighbors)
        found_best = False
        for neighbor in neighbors:
            r, c = neighbor
            current = best[r]
            best[r] = c
            current_conflicts = total_conflicts(best)
            if current_conflicts < best_conflicts and neighbor not in tabu_list:
                best_conflicts = current_conflicts
                tabu_list.append(best[:])
                if len(tabu_list) > tabu_list_size:
                    tabu_list.pop(0)
                found_best = True
                break
            else:
                best[r] = current
        if not found_best:
            best = generate_board(number_of_queens)
            best_conflicts = total_conflicts(best)
    return best

def show_board(board, number_of_queens):
    """
    Printa o tabuleiro com a solução de um tabuleiro
    Parâmetros:
    board -- np.array com a posição de cada rainha no tabuleiro
    number_of_queens -- inteiro com a qnt de damas
    Retorna:
    None.
    """
    board_solution = []
    
    for x in range(number_of_queens):
        board_solution.append(["x"] * number_of_queens)
        
    for i in range(number_of_queens):
        board_solution[board[i]][i]="Q" 
        
    for row in board_solution:
        print (" ".join(row))  
        


def main():   
    number_of_queens = 8    
    solution = tabu_search(number_of_queens)
    print("Uma solução possível para o problema de {}-damas é {}".format(number_of_queens,
                                                                         solution))    
    show_board(solution, number_of_queens)


if __name__ == "__main__":
    main()
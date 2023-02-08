# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:02:47 2023

@author: sergi

"""
import numpy as np
import random
import sys
import time
import matplotlib.pyplot as plt

def conflicts(board):
    """
    Calcula a quantidade de conflitos do tabuleiro 
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

def tabu_search(number_of_queens, tabu_list_size):
    """'
    Realiza a busca tabu
    Parâmetros:
    number_of_queens -- quantidade de damas no tabuleiro 
    tabu_list_size -- tamanho da lista tabu
    Retorna:
    solução encontrada

    """
    
    board = generate_board(number_of_queens)
    best = board
    best_conflicts = conflicts(best)
    tabu_list = []
    iterations = 0
    while best_conflicts != 0:
        print("Iteração {}, menor quantidade de conflitos atual {}".format(iterations, best_conflicts))  
        row, column = random.sample(range(number_of_queens), 2) 
        current = best[row]
        best[row] = column
        current_conflicts = conflicts(best)
        if current_conflicts < best_conflicts:
            best_conflicts = current_conflicts
            tabu_list.append(best)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
        else:
            best[row] = current
            
        neighbors = [[row, column] for c in range(number_of_queens) if c != current]
        random.shuffle(neighbors)
        found_best = False
        for neighbor in neighbors:
            row, column = neighbor[0], neighbor[1]
            current = best[row]
            best[row] = column
            current_conflicts = conflicts(best)
            if current_conflicts < best_conflicts and neighbor not in tabu_list:
                best_conflicts = current_conflicts
                tabu_list.append(best)
                if len(tabu_list) > tabu_list_size:
                    tabu_list.pop(0)
                found_best = True
                break
            else:
                best[row] = current
        if not found_best:
            best = generate_board(number_of_queens)
            best_conflicts = conflicts(best)
        iterations += 1 
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
        
def time_test():
    """
    Testa o tempo médio de execução para o problema de n-rainhas de 4...14
    Plota um gráfico com o tempo médio
    Retorna:
    None
    """
    #[0.001334849999994958, 0.0010872799999987136, 0.0188632699999971, 0.03865948000000401, 0.10604329999999607, 0.3117452799999995, 3.8193840500000023, 9.175329600000003, 37.35564776, 34.212411299999985, 304.13998848999995]
    
    result = []    
    for number_of_queens in range(4,15):   
        print(number_of_queens)
        time_list = []
        for i in range(10):
            start = time.perf_counter()
            tabu_search(number_of_queens, 100)
            end = time.perf_counter()
            time_list.append(end-start)
        result.append(np.mean(time_list))
    print(result)
    X = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    plt.xticks(range(min(X), max(X)+1))

    Y = result
    plt.plot(X, Y)    
    plt.title("Tempo de execução - Busca Tabu")    
    plt.xlabel("Número de damas")
    plt.ylabel("Tempo (em segundos)")
    plt.savefig("time_of_execution.png", dpi = 400)

def main():   
    #time_test()
    
    print("---------------------------------------")
    print("| Selecione a complexidade do problema|")
    print("| 1 - Complexidade baixa - 8 damas    |")
    print("| 2 - Complexidade média - 12 damas   |")
    print("| 3 - Complexidade alta - 16 damas    |")
    print("---------------------------------------")
    selection = int(input("Digite sua opção: "))
    if selection == 1:
        number_of_queens = 8
    elif selection == 2:
        number_of_queens = 12
    elif selection == 3:
        number_of_queens = 16
    else:
        print("Opção inválida")
        sys.exit()
    solution = tabu_search(number_of_queens, 100)
    print("Uma solução possível para o problema de {}-damas é {}".format(number_of_queens,
                                                                         solution))    
    show_board(solution, number_of_queens)
    

if __name__ == "__main__":
    main()
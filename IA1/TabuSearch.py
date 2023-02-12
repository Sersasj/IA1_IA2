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
        #print("Iteração {}, menor quantidade de conflitos atual {}".format(iterations, best_conflicts))  
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
        
        
        neighbors = []
        for row in range(number_of_queens):
            for col in range(number_of_queens):
                if col != board[row]:
                    neighbors.append([row, col])
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
    #[0.001510980000057316, 0.0007360300000982534, 0.009396700000070268, 0.003339529999993829, 0.021564649999891116, 0.03916655000011815, 0.07427775000014662, 0.29064774999988, 0.4338777799997843, 1.2235866399998485, 0.6541262300001108, 1.1291463499999737, 1.53389731999996, 3.243015809999997, 4.662620190000143, 5.724850140000035, 8.598034040000039, 13.966681619999964, 9.650818270000036, 23.682048569999914, 18.096272280000175, 23.467372909999995, 54.86084674999984, 48.83943778999992, 45.40461950999979, 64.13960396000002, 103.98695192000005, 169.64559652000042]
    
    result = []    
    for number_of_queens in range(4,32):   
        print(number_of_queens)
        time_list = []
        for i in range(10):
            start = time.perf_counter()
            tabu_search(number_of_queens, 100)
            end = time.perf_counter()
            time_list.append(end-start)
            print(time_list)
        result.append(np.mean(time_list))
    print(result)
    X1 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    plt.xticks(range(min(X1), max(X1)+1))
    Y1 = result
    
    plt.xticks(fontsize=6)

    plt.plot(X1, Y1)

    plt.title("Tempo de execução - Comparação")    
    plt.xlabel("Número de damas")
    plt.ylabel("Tempo (em segundos)")
    plt.savefig("time_of_execution_tabu.png", dpi = 400)

def main():   
    #time_test()
    
    print("---------------------------------------")
    print("| Selecione a complexidade do problema|")
    print("| 1 - Complexidade baixa - 12 damas    |")
    print("| 2 - Complexidade média - 18 damas   |")
    print("| 3 - Complexidade alta - 22 damas    |")
    print("---------------------------------------")
    selection = int(input("Digite sua opção: "))
    if selection == 1:
        number_of_queens = 12
    elif selection == 2:
        number_of_queens = 18
    elif selection == 3:
        number_of_queens = 24
    else:
        print("Opção inválida")
        sys.exit()
    solution = tabu_search(number_of_queens, 100)
    print("Uma solução possível para o problema de {}-damas é {}".format(number_of_queens,
                                                                         solution))    
    show_board(solution, number_of_queens)
    

if __name__ == "__main__":
    main()
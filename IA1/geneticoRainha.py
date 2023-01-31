from code import interact
from typing import List, Tuple
import random
from statistics import mean, stdev

# fitness = numero de pares de rainhas (i, j), i < j que não se atacam
# assim, o maximo de fitness é um somatório de 1 até (numRainhas - 1)
def calculoFitness(rainhas: List[int]) -> int:
    n = len(rainhas)
    fitness: int = 0
    for i in range(n):
        for j in range(i+1, n):
            if rainhas[i] == rainhas[j]:
                continue
            if j-i == abs(rainhas[i] - rainhas[j]):
                continue
            fitness += 1
    return fitness

# retorna uma tupla com a melhor solucao e o fitness da melhor solucao da populacao
def selecionaMelhorSolucao(populacao: List[List[int]], fitPopulacao: List[int]) -> Tuple[List[int], int]:
    idxMelhorSolucao: int = 0
    melhorFitness: int = fitPopulacao[0]
    for i in range(1, len(fitPopulacao)):
        if fitPopulacao[i] > melhorFitness:
            idxMelhorSolucao = i
            melhorFitness = fitPopulacao[i]
    return tuple((populacao[idxMelhorSolucao], melhorFitness))

# retorna uma lista com o indice do pior fitness da populacao
# caso haja empate, o elemento empatado também é adicionado à lista
def selecionaIdxPiorFitness(fitPopulacao: List[int]) -> List[int]:
    idxPiorFitness: List[int] = [0]
    piorFitness: int = fitPopulacao[0]
    for i in range(1, len(fitPopulacao)):
        if fitPopulacao[i] < piorFitness:
            idxPiorFitness = [i]
            piorFitness = fitPopulacao[i]
        elif fitPopulacao[i] == piorFitness:
            idxPiorFitness.append(i)
    return idxPiorFitness

# na população inicial, cada elemento do indivíduo é único
def gerarPopulacaoInicial(numRainhas: int, tamPopulacao: int) -> List[List[int]]:
    populacao: List[List[int]] = [random.sample(range(numRainhas), numRainhas) for i in range(tamPopulacao)]
    return populacao

# realiza a roleta na lista de disponíveis, nao na fitPopulacao
def resultadoRoleta(fitPopulacao: List[int], disponiveis: List[int], somaFitness: int) -> int:
    sorteado:int = random.randint(0, somaFitness)
    somaAtual: int = 0
    for i in range(len(disponiveis)):
        somaAtual += fitPopulacao[disponiveis[i]]
        if somaAtual >= sorteado:
            return i
    return len(disponiveis)-1

# retorna indices de k individuos para reproducao
def selecaoRoleta(fitPopulacao: List[int], k: int, tamPopulacao: int) -> List[int]:
    disponiveis: List[int] = [i for i in range(tamPopulacao)]
    idxsReproducao: List[int] = []
    somaFitness: int = 0
    for fitness in fitPopulacao:
        somaFitness += fitness
    
    for i in range(k):
        idxSorteado: int = resultadoRoleta(fitPopulacao, disponiveis, somaFitness)
        individuoSorteado = disponiveis[idxSorteado]
        idxsReproducao.append(individuoSorteado)
        somaFitness -= fitPopulacao[individuoSorteado]
        disponiveis[idxSorteado], disponiveis[-1] = disponiveis[-1], disponiveis[idxSorteado]
        disponiveis.pop()

    return idxsReproducao

# Guarda os índices dos elementos de caminho em indices.
# Ex:  caminho = {1, 3, 5, 4, 2}
#     indices[5] contém o índice do elemento 5 => 2
# Assume que indices já tem espaço suficiente alocado.
def inicializaListaIndices(individuo: List[int]) -> List[int]:
    indices: List[int] = [0 for i in range(len(individuo))]
    for i in range(len(individuo)):
        indices[individuo[i]] = i
    return indices 
    
def cycleCrossover(pai1: List[int], pai2: List[int]) -> List[List[int]]:
    pais = [pai1, pai2]
    filhos: List[List[int]] = [[], []]
    indicesPais: List[List[int]] = [[], []]
    for i in range(2):
        outro: int = (i+1) % 2
        filhos[i] = pais[outro]
        indicesPais[outro] = inicializaListaIndices(pais[outro])
        index: int = 0
        while True:
            filhos[i][index] = pais[i][index]; 
            index = indicesPais[outro][filhos[i][index]]
            if index == 0:
                break
    return filhos

# realiza o cruzamento n/2 vezes, sendo n o número de individuos da populacao,
# gerando uma nova populacao de n filhos
def cruzamento(populacao: List[List[int]], idxsReproducao: List[int]) -> List[List[int]]:
    filhos: List[List[int]] = []
    for i in range(len(populacao) // 2):
        idxsPais: List[int] = random.sample(idxsReproducao, 2)
        resultado = cycleCrossover(populacao[idxsPais[0]], populacao[idxsPais[1]])
        filhos.append(resultado[0])
        filhos.append(resultado[1])

    return filhos

# a mutação seleciona 2 posicoes do gene para serem trocadas
def mutacao(populacao: List[List[int]], taxaMutacao: float, numRainhas: int):
    for i in range(len(populacao)):
        randFloat: float = random.random()
        if randFloat <= taxaMutacao:
            rand: List[int] = random.sample(range(numRainhas), 2)
            populacao[i][rand[0]], populacao[i][rand[1]] = populacao[i][rand[1]], populacao[i][rand[0]]

def manutencao(populacao: List[List[int]], fitPopulacao: List[int], filhos: List[List[int]]):
    idxPiorFitness: List[int] = []
    for filho in filhos:
        fitnessFilho: int = calculoFitness(filho)
        if len(idxPiorFitness) < 1:
            idxPiorFitness = selecionaIdxPiorFitness(fitPopulacao)
        if fitnessFilho >= fitPopulacao[idxPiorFitness[-1]]:
            fitPopulacao[idxPiorFitness[-1]] = fitnessFilho
            populacao[idxPiorFitness[-1]] = filho
            idxPiorFitness.pop()

def solveGenetico(numRainhas: int, tamPopulacao: int, maxIteracoes: int, taxaMutacao: float) -> Tuple[int, int]:
    populacao: List[List[int]] = gerarPopulacaoInicial(numRainhas, tamPopulacao)
    fitPopulacao: List[int] = [calculoFitness(individuo) for individuo in populacao]
    melhorSolucao: Tuple[List[int], int] = selecionaMelhorSolucao(populacao, fitPopulacao)
    contIteracoesSemMelhora: int = 0
    iter: int = 0
    maxFitness: int = sum(range(numRainhas))

    while iter < maxIteracoes:   
        idxsReproducao: List[int] = selecaoRoleta(fitPopulacao, tamPopulacao//2, tamPopulacao)
        filhos: List[List[int]] = cruzamento(populacao, idxsReproducao)
        mutacao(filhos, taxaMutacao, numRainhas)
        manutencao(populacao, fitPopulacao, filhos)

        melhorSolucaoAtual: Tuple[List[int], int] = selecionaMelhorSolucao(populacao, fitPopulacao) 
        if melhorSolucaoAtual[1] > melhorSolucao[1]:
            contIteracoesSemMelhora = 0
            melhorSolucao = melhorSolucaoAtual
        else: 
            contIteracoesSemMelhora += 1
        iter += 1
        # print(f"Geracao {iter} / Melhor Resultado: {melhorSolucao[1]}")
        if melhorSolucao[1] == maxFitness:
            break

    # print(f"Solucao: {melhorSolucao[0]}")
    # print(f"Fitness: {melhorSolucao[1]}")
    # print(f"Melhor Fitness Possível: {maxFitness}")

    return tuple((melhorSolucao[1], iter))

def main():
    numRainhas: int = 8
    tamPopulacao: int = 10
    maxIteracoes: int = 10000
    taxaMutacao: float = 0.15

    numExecucoes: int = 100
    listaGeracoes: List[int] = []
    listaSolucoes: List[int] = []
    # random.seed(101)

    for i in range(numExecucoes):
        print(f"Em execucao: {i+1}")
        melhorSolucao, geracoes = solveGenetico(numRainhas, tamPopulacao, maxIteracoes, taxaMutacao)
        listaGeracoes.append(geracoes)
        listaSolucoes.append(melhorSolucao)
        print(f"\tSolucao: {melhorSolucao}; Gerações: {geracoes}")

    
    print(f"\nDados de {numExecucoes} execuções:")
    print(f"Gerações - Média: {mean(listaGeracoes):.3f}; Desvio Padrão: {stdev(listaGeracoes):.3f}")

if __name__ == "__main__":
    main()
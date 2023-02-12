### 9806/01 - APREND.MAQ.E MODEL.CONHECIM.INCERTO
Alunos:
- Gabriel Thiago - RA: 107774
- Sergio Alvarez - RA: 115735

# Problema
Um especialista precisa de ajuda para estimativa das decisões na tabela de um determinado time

Tendo então a decisão de um time para se estar
- Entre o G6 da tabela;
- Entre os Rebaixados; e
- Neutro na classificação.
 
Com base no elenco de jogadores do time, temos:

## Variaveis Aleatórias
- Nota dos jogadores (Overall);
- Velocidade dos jogadores (Pace);
- Chutes ao Gol (shooting);
- Passes completos (Passing); e
- Defesas (Defending).

## Ações Disponíveis
Definir as estimativa de
 
- Time estar no G4   - Classificação de 1 ao 6
- Time estar neutro  - Classificação de 7 ao 15
- Time ser rebaixado - Classificação do 16 ao 20

## Utilidade
- Overall - Utilidade 0.3
- Pace - Utilidade 0.15
- Shooting - Utilidade 0.2
- Passing- Utilidade 0.15
- Defending - Utilidade 0.2

--------------
## Datasets
- [dataset/brasileirao.csv](./dataset/brasileirao.csv)
- [dataset_fifa/players_19.csv](./dataset_fifa/players_19.csv)
- [dataset_fifa/players_20.csv](./dataset_fifa/players_20.csv)
- [dataset_fifa/players_21.csv](./dataset_fifa/players_21.csv)

## Decisão
Ao final é apresentado três casos de teste.
Tendo então os seguintes times a serem estimados a decisão de sua classificação:
- Palmeiras
- Santos
- Atletico Goianiense

-----------------

# Execução

## Requisitos
São necessários os pacotes descritos em [Pacotes Requisitados](./requeriments.txt)
```bash
pip3 install requeriments.txt
```

## Código
Utilize o Python3 para executar o código do [Trabalho](./Trabalho.py)
```python
python3 Trabalho.py
```


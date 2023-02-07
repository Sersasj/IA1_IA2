### Ideia
- Dado três times (Flamengo, Palmeiras e São Paulo) referir as probabilidade dos mesmos de ser campeão (ordem na classificação entre eles, neutro ou rebaixado) do Brasileirão Série A.

### Variaveis aleatórias (Nós de acaso):
- Saldo de Gols
- Histórico no Campeonato
- Overall do Time
- Vitória nos últimos 20 jogos
- Coleçao de Troféus
- Despeza (quando se é rebaixado)
- Bonificação (quando permanece na Série A)

### Decisões (Nós de Decisão):
- Flamengo ser Campeão
- São Paulo ser Campeão
- Palmeiras ser Campeão
- Classificar (? top ?)

### Utilidade (Nós de Utilidade):
 * Útil para se ter a dimensão em qual dos times investir e/ou torcer no ano atual do campeonato.

Exemplo com Estados S:
s1 = {investir, Flamengo, campeão} \
s2 = {não investir, Flamengo, campeão} \
s3 = {investir, São Paulo, campeão} \
s4 = {não investir, Palmeiras, campeão}

U(s1) = 10 \
U(s2) = 0 \
U(s3) = 6 \
U(s4) = 10

Dado que o Flamengo fora campeão, seguido pelo São Paulo e Palmeiras.

---
data (procurar) -
https://www.kaggle.com/datasets/hugomathien/soccer \
ver dado -
https://inloop.github.io/sqlite-viewer/

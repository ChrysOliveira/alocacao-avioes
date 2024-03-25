import random

meta = "h6fAdfSF356D4Gwrd4"

CARACTERES = "abcdefghijklmnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

def faz_lista_inicial():
    lista = []
    for i in range(len(meta)):
        lista.append(random.choice(CARACTERES))
    return lista

def fitness(lista):
    acertos = 0
    for i in range(len(meta)):
        if lista[i] == meta[i]:
            acertos += 1
    return acertos

def mutar(lista):
    nova_lista = list(lista)
    novo_digito = random.choice(CARACTERES)
    indice = random.randint(0, len(meta) - 1)
    nova_lista[indice] = novo_digito
    return nova_lista

def selecao(lista):
    nova_lista = sorted(lista, key=fitness, reverse=True)
    return nova_lista[0:10]

def crossover(populacao, mutada):
    populacao_crossover = []
    for ind1 in populacao:
        for ind2 in mutada:
            # geracao do cross_over
            i = random.randint(0, len(meta) - 1)
            populacao_crossover.append(ind1[0:i] + ind2[i:])
            populacao_crossover.append(ind2[0:i] + ind1[i:])
    return populacao_crossover

print('Iniciando...')
random.seed()

# pooulação inicial
populacao = [faz_lista_inicial() for _ in range(0,10)]

geracoes = 0
while True:
    pop_mutada = [mutar(individuo) for individuo in populacao]
    pop_crossover = crossover(populacao, pop_mutada)

    populacao = selecao(populacao + pop_mutada + pop_crossover)
    
    geracoes += 1
    if geracoes % 50 == 0:
        print(''.join(populacao[0]), geracoes)
    # critério de parada
    if fitness(populacao[0]) == len(meta):
        break
print('Finalizado!')
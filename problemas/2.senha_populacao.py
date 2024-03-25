import random

def faz_lista_inicial():
    lista = []

    for i in range(84):
        if i in range(10):
            lista.append([i, "SP", "RJ", 0, 1.0])
        elif i in range(10, 16):
            lista.append([i, "SP", "BR", 0, 2.0])
        elif i in range(16, 24):
            lista.append([i, "SP", "BH", 0, 1.5])
        elif i in range(24, 34):
            lista.append([i, "RJ", "SP", 0, 1.0])
        elif i in range(34, 39):
            lista.append([i, "RJ", "BR", 0, 2.0])
        elif i in range(39, 45):
            lista.append([i, "RJ", "BH", 0, 1.5])
        elif i in range(45, 51):
            lista.append([i, "BR", "SP", 0, 2.0])
        elif i in range(51, 56):
            lista.append([i, "BR", "RJ", 0, 2.0])
        elif i in range(56, 63):
            lista.append([i, "BR", "BH", 0, 1.5])
        elif i in range(63, 71):
            lista.append([i, "BH", "SP", 0, 1.5])
        elif i in range(71, 77):
            lista.append([i, "BH", "RJ", 0, 1.5])
        elif i in range(77, 84):
            lista.append([i, "BH", "BR", 0, 1.5])

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

print('Iniciando...')
random.seed()

# pooulação inicial
populacao = [faz_lista_inicial() for _ in range(0,10)]

geracoes = 0
while True:
    lista_mutada = [mutar(individuo) for individuo in populacao]
    populacao = selecao(populacao + lista_mutada)

    geracoes += 1
    if geracoes % 50 == 0:
        print(''.join(populacao[0]), geracoes)
    # critério de parada
    if fitness(populacao[0]) == len(meta):
        break
print('Finalizado!')
import random
from copy import copy

quantidade_max_avioes = 84
#de 0 ate 24h em minutos pulando de 30 em 30 minutos
horarios_possiveis_saida = [i for i in range(0, 1440, 30)]


def faz_lista_inicial():
    lista = []

    for i in range(84):
        if i in range(10):
            lista.append([i, "SP", "RJ", 0, 60])
        elif i in range(10, 16):
            lista.append([i, "SP", "BR", 0, 120])
        elif i in range(16, 24):
            lista.append([i, "SP", "BH", 0, 90])
        elif i in range(24, 34):
            lista.append([i, "RJ", "SP", 0, 60])
        elif i in range(34, 39):
            lista.append([i, "RJ", "BR", 0, 120])
        elif i in range(39, 45):
            lista.append([i, "RJ", "BH", 0, 90])
        elif i in range(45, 51):
            lista.append([i, "BR", "SP", 0, 120])
        elif i in range(51, 56):
            lista.append([i, "BR", "RJ", 0, 120])
        elif i in range(56, 63):
            lista.append([i, "BR", "BH", 0, 90])
        elif i in range(63, 71):
            lista.append([i, "BH", "SP", 0, 90])
        elif i in range(71, 77):
            lista.append([i, "BH", "RJ", 0, 90])
        elif i in range(77, 84):
            lista.append([i, "BH", "BR", 0, 90])

    return lista

def mutar(individuo):
    novo_individuo = list(individuo)

    for alocacao in novo_individuo:

        alocacao[0] = random.randint(0, quantidade_max_avioes)

        novo_horario = random.randint(0, len(horarios_possiveis_saida) - 1)
        alocacao[3] = horarios_possiveis_saida[novo_horario]

    return novo_individuo

def fitness(individuo):
    punicao_total = 0
    avioes_visitados = set()
    sorted(individuo, key=lambda alocacao: alocacao[3])

    for alocacao in individuo:
        individuo_copia_sem_atual = list(copy(individuo))
        individuo_copia_sem_atual.remove(alocacao)

        aviao = alocacao[0]
        aviao_tempo_ocupado = [alocacao[3] - 60, alocacao[4] + 30]

        # verifica se a manutencao do mesmo dia
        if aviao_tempo_ocupado[0] < 0 or aviao_tempo_ocupado[0] > 1440:
            punicao_total = float("-inf")
            break

        # valida se tem conflito de aviao nos voos -> mesmo aviao em dois voos diferentes no mesmo horario
        for prox_alocacao in individuo_copia_sem_atual:
            if prox_alocacao[0] == aviao:
                prox_aviao_tempo_ocupado = [prox_alocacao[3] - 60, prox_alocacao[4] + 30]

                if max(aviao_tempo_ocupado) < min(prox_aviao_tempo_ocupado) or min(aviao_tempo_ocupado) > max(prox_aviao_tempo_ocupado):
                    punicao_total = float("-inf")
                    break
                elif alocacao[2] != prox_alocacao[1]:
                    punicao_total = float("-inf")
                    break

        if punicao_total == float("-inf"):
            break

        #verifica a quantidade total do tempo alocado de um aviao e aplica a punicao respectiva
        if aviao in avioes_visitados:
            continue
        else:
            avioes_visitados.add(aviao)
            tempo_alocacao_total = aviao_tempo_ocupado[1] - aviao_tempo_ocupado[0]

            for prox_alocacao in individuo_copia_sem_atual:
                if prox_alocacao[0] == aviao:
                    prox_aviao_tempo_ocupado = [prox_alocacao[3] - 60, prox_alocacao[4] + 30]
                    tempo_alocacao_total += prox_aviao_tempo_ocupado[1] - prox_aviao_tempo_ocupado[0]

            tempo_parado = (1440 - tempo_alocacao_total) * -1

            punicao_total += tempo_parado

    return punicao_total

def selecao(lista):
    nova_lista = sorted(lista, key=fitness, reverse=False)
    return nova_lista[0:20]

print('Iniciando...')
random.seed()

# pooulação inicial
populacao = [faz_lista_inicial() for _ in range(0, 100)]

geracoes = 0
while True:
    lista_mutada = [mutar(individuo) for individuo in populacao]
    populacao = selecao(populacao + lista_mutada)

    geracoes += 1

    if geracoes % 50 == 0:
       print(populacao)
       quantidade_max_avioes -= 1
    # critério de parada
    if quantidade_max_avioes == 0:
        melhor_individuo = populacao[0]
        print(f"Melhor solucao {sorted(melhor_individuo, key=lambda alocacao: alocacao[3])}")
        break

print('Finalizado!')
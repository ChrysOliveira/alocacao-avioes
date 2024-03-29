import random
import copy

quantidade_max_avioes = 84
# de 0 ate 24h em minutos pulando de 30 em 30 minutos
horarios_possiveis_saida = [i for i in range(60, 1440, 30)]


def faz_lista_inicial():
    lista = []

    for i in range(84):
        if i in range(10):
            lista.append([i, "SP", "RJ", 0, 60, 0])
        elif i in range(10, 16):
            lista.append([i, "SP", "BR", 0, 120, 0])
        elif i in range(16, 24):
            lista.append([i, "SP", "BH", 0, 90, 0])
        elif i in range(24, 34):
            lista.append([i, "RJ", "SP", 0, 60, 0])
        elif i in range(34, 39):
            lista.append([i, "RJ", "BR", 0, 120, 0])
        elif i in range(39, 45):
            lista.append([i, "RJ", "BH", 0, 90, 0])
        elif i in range(45, 51):
            lista.append([i, "BR", "SP", 0, 120, 0])
        elif i in range(51, 56):
            lista.append([i, "BR", "RJ", 0, 120, 0])
        elif i in range(56, 63):
            lista.append([i, "BR", "BH", 0, 90, 0])
        elif i in range(63, 71):
            lista.append([i, "BH", "SP", 0, 90, 0])
        elif i in range(71, 77):
            lista.append([i, "BH", "RJ", 0, 90, 0])
        elif i in range(77, 84):
            lista.append([i, "BH", "BR", 0, 90, 0])

    return lista


def mutar(individuo):
    novo_individuo = copy.deepcopy(list(individuo))

    aviao_e_ultimo_horario = dict()
    aviao_e_ultimo_destino = dict()
    ultimo_destino = ""

    for alocacao in novo_individuo:

        alocacao[0] = random.randint(0, quantidade_max_avioes)

    novo_individuo_ordenado = sorted(novo_individuo, key=lambda alocacao: (alocacao[0], alocacao[3]))

    for alocacao in novo_individuo_ordenado:

        if alocacao[0] not in aviao_e_ultimo_destino:
            aviao_e_ultimo_destino[alocacao[0]] = alocacao[2]
        else:
            if(alocacao[1] != ultimo_destino):
                cross_over(novo_individuo_ordenado, alocacao, ultimo_destino)

        ultimo_destino = alocacao[2]

    for alocacao in novo_individuo_ordenado:

        if alocacao[0] not in aviao_e_ultimo_horario:
            novo_horario = 60
            alocacao[3] = novo_horario
            alocacao[5] = alocacao[3] + 30 + alocacao[4]
            aviao_e_ultimo_horario[alocacao[0]] = alocacao[5] + 60
        else:

            # novo_horario = random.randint(0, len(horarios_possiveis_saida) - 1)
            novo_horario = aviao_e_ultimo_horario[alocacao[0]]
            # alocacao[3] = horarios_possiveis_saida[novo_horario]
            alocacao[3] = novo_horario
            alocacao[5] = alocacao[3] + 30 + alocacao[4]
            aviao_e_ultimo_horario[alocacao[0]] = alocacao[5] + 60

    # items = sorted(aviao_e_ultimo_horario.items(), key=lambda item:item[0])
    #
    # print(items)
    return novo_individuo_ordenado


def cross_over(individuo, alocacao, nova_origem):

    enable = False

    for finder in individuo:

        if enable:
            if finder[1] == nova_origem:
                alocacao[1], finder[1] = finder[1], alocacao[1]
                alocacao[2], finder[2] = finder[2], alocacao[2]
                alocacao[4], finder[4] = finder[4], alocacao[4]
                break

        if finder == alocacao:
            enable = True


def fitness(individuo):
    punicao_total = 0
    avioes_visitados = set()
    # individuo = sorted(individuo, key=lambda alocacao: alocacao[3])
    individuo_copia_sem_atual = copy.deepcopy(list(individuo))

    for alocacao in individuo:
        individuo_copia_sem_atual.remove(alocacao)

        aviao = alocacao[0]
        aviao_tempo_ocupado = [alocacao[3] - 60, alocacao[5]]

        # verifica se a manutencao do mesmo dia
        if aviao_tempo_ocupado[0] < 0 or aviao_tempo_ocupado[0] > 1440 or aviao_tempo_ocupado[1] >= 1440:
            # punicao_total = float("-inf")
            punicao_total = -1000001
            break

        # valida se tem conflito de aviao nos voos -> mesmo aviao em dois voos diferentes no mesmo horario
        for prox_alocacao in individuo_copia_sem_atual:
            if prox_alocacao[0] == aviao:
                prox_aviao_tempo_ocupado = [prox_alocacao[3] - 60, prox_alocacao[5]]
                # or min(aviao_tempo_ocupado) > max(prox_aviao_tempo_ocupado)

                # trocamos o menor por maior
                # =-=-=-=-=-=-=-=-=-=-=-=-=-=- TODOS OS INDIVIDUOS ESTAO MORRENDO AQUI
                if max(aviao_tempo_ocupado) > min(prox_aviao_tempo_ocupado):
                    # punicao_total = float("-inf")
                    punicao_total = -1000002
                    break
                elif alocacao[2] != prox_alocacao[1]:
                    # punicao_total = float("-inf")
                    punicao_total = -1000003
                    break
                else:
                    break
                # =-=-=-=-=-=-=-=-=-=-=-=-=-=- AQUI ELE JA TA MORTO

        # if punicao_total == float("-inf"):
        if punicao_total < -1000000:
            break

        # verifica a quantidade total do tempo alocado de um aviao e aplica a punicao respectiva
        if aviao in avioes_visitados:
            continue
        else:
            avioes_visitados.add(aviao)
            tempo_alocacao_total = aviao_tempo_ocupado[1] - aviao_tempo_ocupado[0]

            for prox_alocacao in individuo_copia_sem_atual:
                if prox_alocacao[0] == aviao:
                    prox_aviao_tempo_ocupado = [prox_alocacao[3] - 60, prox_alocacao[5]]
                    tempo_alocacao_total += prox_aviao_tempo_ocupado[1] - prox_aviao_tempo_ocupado[0]

            tempo_parado = (1440 - tempo_alocacao_total) * -1

            punicao_total += tempo_parado

    return punicao_total


def selecao(lista):
    nova_lista = sorted(lista, key=fitness, reverse=True)
    return nova_lista[0:10]


def ordena_individuos_da_populacao(populacao):
    populacao_com_individuos_ordenados = []
    for individuo in populacao:
        individuo = sorted(individuo, key=lambda alocacao: (alocacao[0], alocacao[3]))
        populacao_com_individuos_ordenados.append(individuo)

    return populacao_com_individuos_ordenados


print('Iniciando...')
random.seed()

# pooulação inicial
populacao = [faz_lista_inicial() for _ in range(10)]

geracoes = 0
while True:
    lista_mutada = [mutar(individuo) for individuo in populacao]
    lista_unificada = populacao + lista_mutada
    lista_unificada = ordena_individuos_da_populacao(lista_unificada)
    populacao = selecao(lista_unificada)

    geracoes += 1

    if geracoes % 100 == 0:
        quantidade_max_avioes -= 1
        ordenado_por_aviao_e_horario = sorted(populacao[0], key=lambda alocacao: (alocacao[0], alocacao[3]))
        print(f"Populacao no momento: {ordenado_por_aviao_e_horario} \nQuantidade de avioes: {quantidade_max_avioes}"
              f"\nFitness do melhor: {fitness(ordenado_por_aviao_e_horario)}\n\n")
    # critério de parada
    if geracoes == 8400:
        melhor_individuo = populacao[0]
        print(f"Melhor solucao {sorted(melhor_individuo, key=lambda alocacao: (alocacao[0], alocacao[3]))}"
              f"\nFitness melhor solucao: {fitness(melhor_individuo)}")
        break

print('Finalizado!')

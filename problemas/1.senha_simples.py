import random

meta = "h6fAdfSF356D4Gwrd4fgSKYRfgEBG578T2HYGIW74Y5W7"

CARACTERES = "abcdefghijklmnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%ˆ&*()-=+[];:,.<>/?~\{\}\\|_"

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

print('Iniciando...')
random.seed()
melhor_lista = faz_lista_inicial()
melhor_nota = fitness(melhor_lista)

tentativas = 0
print(''.join(melhor_lista), melhor_nota, tentativas)

while True:
    lista_nova = mutar(melhor_lista)
    nota_nova = fitness(lista_nova)
    tentativas += 1

    if nota_nova <= melhor_nota:
        continue
    
    print(''.join(lista_nova), nota_nova, tentativas)
    if nota_nova == len(meta):
        break
    
    melhor_lista = list(lista_nova)
    melhor_nota = nota_nova
print('Finalizado!')
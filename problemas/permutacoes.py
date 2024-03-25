from itertools import permutations
import random
  
# Get all permutations of length 2 
# and length 2 
perm = permutations(["Escondidos",
    "Santa Paula",
    "Campos",
    "Riacho de Fevereiro",
    "Algas",
    "Além-do-Mar",
    "Guardião",
    "Foz da Água Quente",
    "Leão",
    "Granada",
    "Lagos",
    "Ponte-do-Sol",
    "Porto",
    "Limões"], 2)
  
random.seed()

# Print the obtained permutations 

visitadas = []

for i in list(perm): 
    if i in visitadas:
        continue
    tempo = random.randint(1, 10)
    custo = tempo * random.randint(50, 150)
    a = (i[0],i[1],str(tempo),str(custo))
    visitadas.append((i[1],i[0]))
    print(",".join(a)) 
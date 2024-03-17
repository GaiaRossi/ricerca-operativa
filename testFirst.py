# TODO: inserire la durata dei test e tutte le caratteristiche neccessarie dei nodi

import networkx as nx
import matplotlib.pyplot as plt
import itertools
import time

def isFinito():
    finito = True
    for i in range(n_pazienti):
        if finito != False:
            test = tests[i]
            for j in range(len(test)):
                label = f"{pazienti[i]}t{test[j]}"
                finito = G.nodes[label]["completato"]
    return finito

def crea_clique(test):
    da_collegare = []
    for nodo in G.nodes:
        if test in nodo:
            da_collegare.append(nodo)
    
    permutazioni = list(itertools.permutations(da_collegare))
    n_permutazioni = len(permutazioni)

    for i in range(n_permutazioni):
        curr = permutazioni[i]
        for j in range(len(curr) - 1):
            G.add_edge(curr[j], curr[j+1], color=lista_color[int(test[-1]) - 1])
            
def trova_path(start, finish):
    path = []
    next = start
    path.append(next)

    while next != finish:
        neigh = [n for n in list(nx.neighbors(G, next)) if f"t{start[-2]}" in n and G.nodes[n]["completato"] == False]

        if neigh == []:
            next = finish
            path.append(next)
        
        else:
            # TODO: implementare la scelta del prossimo nodo
            next = neigh[0]
            path.append(next)
            G.nodes[next]["completato"] = True

    return path

def prossimo_test(neigh):
    # scegli il paziente che libererebbe prima
    # la saletta (makespan minore)
    # elenco i pazienti che vedo direttamente
    pazienti_vicino = []
    for vicino in neigh:
        if "p" in vicino:
            # estraggo la label
            label = vicino[:2]
            pazienti_vicino.append(label)

    # TODO: utilizzare list comprehension per rendere piu
            # semplice il pezzo sotto
    # [n for n in list(nx.neighbors(G, curr)) 
                #   if f"t{i+1}" in n and
                #   G.nodes[n]["completato"] == False and
                #   G.nodes[n]["occupato"] == False and
                #   G.nodes[n]["prec_ok"] == True
                # ]
    # calcolo la somma dei tempi dei test rimanenti
    somme = {}
    for paziente in pazienti_vicino:
        index = int(paziente[-1]) - 1
        tutti_test_per_paziente = tests[index]
        # guardo i test che devono essere ancora eseguiti
        tot = 0
        for test in tutti_test_per_paziente:
            label = f"{paziente}t{test}"
            tot += G.nodes[label]["durata"]
        somme[paziente] = tot

    # prende il primo elemento del dizionario
    min = None
    min_durata = 10000000
    for paziente in somme.items():
        if paziente[1] < min_durata:
            min_durata = paziente[1]
            min = paziente

    nodo = f"{min[0]}t{neigh[0][-1]}"
    return nodo
    

# generare i nodi che servono

# nodo TiPj
n_pazienti = 4
pazienti = ["p1", "p2", "p3", "p4"]
lista_tests = ["t1", "t2", "t3", "t4", "t5"]
lista_durate = [2, 5, 3, 4, 7]
lista_color = ['r', 'g', 'b', 'c', 'y']
operatori = ["o1", "o2", "o3", "o4", "o5"]
n_operatori = n_test = 5
# facciamo che la lista segna l ordine
tests = [
    [1, 2, 5, 3],
    [1, 3, 4, 2],
    [1, 2, 3, 4, 5],
    [2, 3, 1]
]

G = nx.DiGraph()

# generazione tutti i nodi
for i in range(n_pazienti):
    test = tests[i]
    for j in range(len(test)):
        indice_test = test[j] - 1
        durata = lista_durate[indice_test]
        G.add_node(f"{pazienti[i]}t{test[j]}", completato=False, durata=durata, start=-1, finish=-1, occupato=False, prec_ok=False)

# generazione archi per precedenze
for i in range(n_pazienti):
    test = tests[i]
    #print(f"Paziente {pazienti[i]}:")
    for j in range(len(test)-1):
        #print(f"{test[j]} -> {test[j+1]}")
        G.add_edge(f"{pazienti[i]}t{test[j]}", f"{pazienti[i]}t{test[j+1]}", color="k")

# clique operatori
for test in lista_tests:
    crea_clique(test)

# nodo operatore di inizio e fine
for o in operatori:
    G.add_node(f"{o}s", completato=True)
    G.add_node(f"{o}f", completato=False)

# colleghiamo nodo operatore con tutti i nodi
# dei test che deve svolgere
for i in range(n_operatori):
    nodi_test = [n for n in G.nodes if f"t{i+1}" in n]
    for nodo in nodi_test:
        G.add_edge(f"o{i+1}s", nodo, color="k")

# da i test fino al nodo operatore finale
for i in range(n_operatori):
    nodi_test = [n for n in G.nodes if f"t{i+1}" in n]
    for nodo in nodi_test:
        G.add_edge(nodo, f"o{i+1}f", color="k")

# trovare un percorso da nodo operatore iniziale a finale
# che passi tutti i test che deve svolgere
# e che non ci siano cicli

# for i in range(n_operatori):
#     start = f"{operatori[i]}s"
#     finish = f"{operatori[i]}f"

#     path = trova_path(start, finish)
#     print(f"Operatore {operatori[i]} -> {path}")

# sol 1
ultimi_nodi = ["o1f", "o2f", "o3f", "o4f", "o5f"]
finito = False
step = 0
path = [
    ["o1s"],
    ["o2s"],
    ["o3s"],
    ["o4s"],
    ["o5s"]
]

while not finito:
    time.sleep(1)
    print(f"Current step {step}")

    # computiamo le precedenze
    for i in range(n_pazienti):
        test = tests[i]
        for j in range(len(test)):
            if j == 0:
                label = f"{pazienti[i]}t{test[j]}"
                G.nodes[label]["prec_ok"] = True
            else:
                label = f"{pazienti[i]}t{test[j-1]}"
                ok = G.nodes[label]["completato"]
                label = f"{pazienti[i]}t{test[j]}"
                G.nodes[label]["prec_ok"] = ok
                

    for i in range(n_operatori):
        # computiamo per tutti i nodi se sono attualmente occupati
        for indice_paziente in range(n_pazienti):
            numero_paziente = indice_paziente + 1
            nodi_paziente = [n for n in G.nodes if f"p{numero_paziente}" in n]
            # cerchiamo almeno un nodo che occupa il paziente
            paziente_occupato = False
            for n in nodi_paziente:
                if paziente_occupato == True:
                    continue

                if step < G.nodes[n]["finish"]:
                    paziente_occupato = True

            if paziente_occupato == True:
                # segno i nodi occupati
                for n in nodi_paziente:
                    G.nodes[n]["occupato"] = True

            else:
                for n in nodi_paziente:
                    G.nodes[n]["occupato"] = False

        curr_path = path[i]
        curr = path[i][-1]
        
        neigh = [n for n in list(nx.neighbors(G, curr)) 
                  if f"t{i+1}" in n and
                  G.nodes[n]["completato"] == False and
                  G.nodes[n]["occupato"] == False and
                  G.nodes[n]["prec_ok"] == True
                ]
        print(f"Nodo corrente: {curr}")
        print(neigh)

        if "p" in curr:
            # se non puoi fare la scelta in questo istante
            # vai alla prossima iterazione
            if step < G.nodes[curr]["finish"]:
                continue

        if neigh != []:
            next = prossimo_test(neigh)
            G.nodes[next]["start"] = step
            G.nodes[next]["finish"] = step + G.nodes[next]["durata"]
            curr_path.append(next)
            G.nodes[next]["completato"] = True

    # conclusione ciclo
    finito = isFinito()
    step += 1

# append nodo finale
for p in path:
    label = p[0].replace("s", "f")
    p.append(label)

for p in path:
    print(p)

pos = nx.spring_layout(G)
colors = nx.get_edge_attributes(G,'color').values()
styles = nx.get_edge_attributes(G,'style').values()
durate = nx.get_node_attributes(G, 'durata').values()
inizi = nx.get_node_attributes(G, 'start').values()
fine = nx.get_node_attributes(G, 'finish').values()
nodi = [n for n in G.nodes if "p" in n]
for n in nodi:
    start = G.nodes[n]["start"]
    finish = G.nodes[n]["finish"]
    print(f"Nodo: {n}, start: {start} -> finish: {finish}")
nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color=colors)
plt.savefig("image.png")
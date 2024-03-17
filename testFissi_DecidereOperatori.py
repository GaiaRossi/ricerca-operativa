import networkx as nx
import matplotlib.pyplot as plt
import itertools
import time

def numero_pazienti_occupati():
    pazienti_occupati = 0
    for _, stato in stato_paziente.items():
        if stato == "OCCUPATO":
            pazienti_occupati += 1

    return pazienti_occupati

def check_tutti_test_completati():
    tutti_test_completati = True
    for i in range(n_pazienti):
        if tutti_test_completati != False:
            test = tests[i]
            for j in range(len(test)):
                label = f"{pazienti[i]}t{test[j]}"
                tutti_test_completati = G.nodes[label]["completato"]
    return tutti_test_completati

def crea_clique_tra_test_stesso_operatore(test):
    da_collegare = []
    for nodo in G.nodes:
        if test in nodo:
            da_collegare.append(nodo)
    
    permutazioni = list(itertools.permutations(da_collegare))
    n_permutazioni = len(permutazioni)

    for i in range(n_permutazioni):
        numero_operatore_corrente = permutazioni[i]
        for j in range(len(numero_operatore_corrente) - 1):
            G.add_edge(numero_operatore_corrente[j], numero_operatore_corrente[j+1], color=lista_color[int(test[-1]) - 1])

def prossimo_test_SPT(neigh):
    label_pazienti_vicino = []
    for vicino in neigh:
        label = vicino[:2]
        label_pazienti_vicino.append(label)

    # TODO: utilizzare list comprehension per rendere piu
            # semplice il pezzo sotto
    # calcolo la somma dei tempi dei test rimanenti
    somme = {}
    for label_paziente in label_pazienti_vicino:
        index = int(label_paziente[-1]) - 1
        tutti_test_per_paziente = tests[index]
        # guardo i test che devono essere ancora eseguiti
        tempo_rimanente = 0
        for test in tutti_test_per_paziente:
            label_nodo = f"{label_paziente}t{test}"
            tempo_rimanente += G.nodes[label_nodo]["durata"]
        somme[label_paziente] = tempo_rimanente

    min_label_paziente = None
    min_tempo_restante = 10000000
    for label_paziente, tempo_restante in somme.items():
        if tempo_restante < min_tempo_restante:
            min_tempo_restante = tempo_restante
            min_label_paziente = label_paziente

    indice_test = neigh[0][-1]
    nodo = f"{min_label_paziente}t{indice_test}"
    return nodo

def set_stato_pazienti():
    for paziente in pazienti:
        nodi_paziente = [n for n in G.nodes if f"{paziente}" in n]
        paziente_completato = "COMPLETATO"
        for nodo in nodi_paziente:
            if paziente_completato == "COMPLETATO":
                if not G.nodes[nodo]["completato"]:
                    paziente_completato = "LIBERO"

        stato_paziente[paziente] = paziente_completato


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
            stato_paziente[f"p{numero_paziente}"] = "OCCUPATO"
            # segno i nodi occupati
            for n in nodi_paziente:
                G.nodes[n]["occupato"] = True

        else:
            for n in nodi_paziente:
                G.nodes[n]["occupato"] = False

def check_precedenze():
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

# nodo TiPj
n_pazienti = 4
pazienti = ["p1", "p2", "p3", "p4"]
stato_paziente = {}
lista_tests = ["t1", "t2", "t3", "t4", "t5"]
lista_durate = [2, 5, 3, 4, 7]
lista_color = ['r', 'g', 'b', 'c', 'y']
operatori = ["o1", "o2", "o3", "o4", "o5"]
n_operatori = n_test = 5
tests = [
    [1, 2, 5, 3],
    [1, 3, 4, 2],
    [1, 2, 3, 4, 5],
    [2, 3, 1]
]
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


G = nx.DiGraph()

# setup dizionario stato
# possibili valori:
# - LIBERO
# - OCCUPATO
# - COMPLETATO
for paziente in pazienti:
    stato_paziente[paziente] = "LIBERO"

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
    crea_clique_tra_test_stesso_operatore(test)

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

while not finito:
    time.sleep(1)
    print(f"numero_operatore_correnteent step {step}")

    check_precedenze()
    set_stato_pazienti()

    for i in range(n_operatori):
        sale_occupate = numero_pazienti_occupati()
        print(f"Sale occupate {sale_occupate}")
        if sale_occupate <= 3:
            percorso_operatore_corrente = path[i]
            nodo_corrente = path[i][-1]
            
            neigh = [n for n in list(nx.neighbors(G, nodo_corrente)) 
                    if f"t{i+1}" in n and
                    G.nodes[n]["completato"] == False and
                    G.nodes[n]["occupato"] == False and
                    G.nodes[n]["prec_ok"] == True
                    ]
            print(f"Nodo corrente: {nodo_corrente}")
            print(neigh)

            if "p" in nodo_corrente:
                # per evitare che acceda a finish dei nodi operatore
                if step < G.nodes[nodo_corrente]["finish"]:
                    continue

            if neigh != []:
                next = prossimo_test_SPT(neigh)
                G.nodes[next]["start"] = step
                G.nodes[next]["finish"] = step + G.nodes[next]["durata"]
                percorso_operatore_corrente.append(next)
                G.nodes[next]["completato"] = True

    # conclusione ciclo
    finito = check_tutti_test_completati()
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
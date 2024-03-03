import networkx as nx
import matplotlib.pyplot as plt
import itertools

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

# generare i nodi che servono

# nodo TiPj
n_pazienti = 3
pazienti = ["p1", "p2", "p3"]
lista_tests = ["t1", "t2", "t3"]
lista_color = ['r', 'g', 'b']
operatori = ["o1", "o2", "o3"]
n_operatori = n_test = 3
# facciamo che la lista segna l ordine
tests = [
    [1, 2],
    [1, 3],
    [1, 2, 3]
]

G = nx.DiGraph()

# generazione tutti i nodi
for i in range(n_pazienti):
    test = tests[i]
    for j in range(len(test)):
        G.add_node(f"{pazienti[i]}t{test[j]}", completato=False)

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
    G.add_node(f"{o}s")
    G.add_node(f"{o}f")

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

for i in range(n_operatori):
    start = f"{operatori[i]}s"
    finish = f"{operatori[i]}f"

    path = trova_path(start, finish)
    print(f"Operatore {operatori[i]} -> {path}")

pos = nx.spring_layout(G)
colors = nx.get_edge_attributes(G,'color').values()
styles = nx.get_edge_attributes(G,'style').values()
nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color=colors)
plt.savefig("image.png")
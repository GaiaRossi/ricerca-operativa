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

# generare i nodi che servono
# nodo TiPj

n_pazienti = 3
pazienti = ["p1", "p2", "p3"]
lista_tests = ["t1", "t2", "t3"]
lista_color = ['r', 'g', 'b']
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
        G.add_node(f"{pazienti[i]}t{test[j]}")

# generazione archi per precedenze
for i in range(n_pazienti):
    test = tests[i]
    #print(f"Paziente {pazienti[i]}:")
    for j in range(len(test)-1):
        #print(f"{test[j]} -> {test[j+1]}")
        G.add_edge(f"{pazienti[i]}t{test[j]}", f"{pazienti[i]}t{test[j+1]}", color="k")

# percorso operatori
for test in lista_tests:
    crea_clique(test)

pos = nx.spring_layout(G)
colors = nx.get_edge_attributes(G,'color').values()
nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color=colors)
plt.savefig("image.png")
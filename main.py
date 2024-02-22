import networkx as nx
import matplotlib.pyplot as plt

# Creazione di un nuovo grafo
G = nx.DiGraph()

# Aggiunta dei nodi pazienti
G.add_node('P1', tests=[1, 3, 5])
G.add_node('P2', tests=[2, 4])
G.add_node('P3', tests=[5])

# Aggiunta dei nodi test
G.add_node('T1', paziente = 'P1')
G.add_node('T3', paziente = 'P1')
G.add_node('T5', paziente = 'P1')

G.add_node('T2', paziente = 'P2')
G.add_node('T4', paziente = 'P2')

G.add_node('T5', paziente = 'P3')

# Aggiunta dei nodi operatori
for i in range(1, 6):
    G.add_node('Operator'+str(i), test=i)

# Aggiunta degli archi tra operatori e pazienti
for patient in ['P1', 'P2', 'P3']:
    for test in G.nodes[patient]['tests']:
        for operator in G.nodes:
            if 'Operator' in operator and G.nodes[operator]['test'] == test:
                G.add_edge(operator, patient)

# Aggiunta degli archi tra test e pazienti
for node in G.nodes:
    if 'T' in node:
        G.add_edge(G.nodes[node]['paziente'], node)
        

# Definizione dell'ordine dei nodi per la navigazione
order = ['Operator1', 'Operator2', 'Operator3', 'Operator4', 'Operator5', 'P1', 'P2', 'P3']

# Navigazione del grafo secondo l'ordine specifico
for node in order:
    if node in G.nodes():
        print("Node:", node)
        successors = list(G.successors(node))
        if successors:
            print("Successors:", successors)
        print()

# Disegno del grafo
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
plt.savefig("image.png")
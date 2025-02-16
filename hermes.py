class Graph:
    def __init__(self):
        self.graph = {}
        self.nodes = []

    def add_node(self, node):
        if not node in self.graph:
            self.graph[node] = []
            self.nodes.append(node)

    def add_edge(self, edge):
        node1 = edge.get_node1()
        node2 = edge.get_node2()
        self.add_node(node1)
        self.add_node(node2)
        present = False
        for sublist in self.graph[node1]:
            if node2 in sublist:
                present = True
                break
        if not present:
            self.graph[node1].append([node2, edge.get_time()])
        for sublist in self.graph[node2]:
            if node1 in sublist:
                present = True
                break
        if not present:
            self.graph[node2].append([node1, edge.get_time()])

    def dijkstra(self, inicio, final):
        if not inicio in self.nodes or not final in self.nodes:
            return False
        actual = inicio
        noVisitados = list(self.nodes)
        padres = {}
        visitados = {}
        distancias = {actual: 0}
        for i in self.nodes:
            if i != actual:
                distancias[i] = float("inf")
            padres[i] = None
            visitados[i] = False

        while len(noVisitados) > 0:
            for vecino in self.graph[actual]:
                if not visitados[vecino[0]]:
                    if distancias[actual] + vecino[1] < distancias[vecino[0]]:
                        distancias[vecino[0]] = distancias[actual] + vecino[1]
                        padres[vecino[0]] = actual
            visitados[actual] = True
            noVisitados.remove(actual)

            if len(noVisitados) > 0:
                m = distancias[noVisitados[0]]
                actual = noVisitados[0]
                for e in noVisitados:
                    if m > distancias[e]:
                        m = distancias[e]
                        actual = e

        camino = []
        actual = final
        while actual != None:
            camino.insert(0, actual)
            actual = padres[actual]
        return [camino, distancias[final]]


class Edge:
    def __init__(self, node1, node2, time):
        self.node1 = node1
        self.node2 = node2
        self.time = time

    def get_node1(self):
        return self.node1

    def get_node2(self):
        return self.node2

    def get_time(self):
        return self.time


def siguiente_letra(alfabeto, letra):
    if not letra in alfabeto:
        return
    if letra == alfabeto[-1]:
        return "A"
    return chr(ord(letra) + 1)


graph = Graph()

# Arrecifes
arrecifes = input().split()

entrada = input().split()
# Cantidad de Caminos
K = int(entrada[0])
# Tolerancia de Sueño de Hermes
S = int(entrada[1])

# K Lineas
for i in range(int(K)):
    entrada = input().split()
    X = entrada[0]
    Y = entrada[1]
    T = int(entrada[2])
    graph.add_edge(Edge(X, Y, T))

# Arrecifes a visitar
arrecifes_a_visitar = input().split()

# Arrecife de inicio
arrecife_inicio = input()

# Tiempo Total
tiempo_total = 0

for arrecife_a_visitar in arrecifes_a_visitar:
    while True:
        resultadodijkstra = graph.dijkstra(arrecife_inicio, arrecife_a_visitar)
        camino_recorrido = resultadodijkstra[0]
        tiempo_recorrido = resultadodijkstra[1]
        camino_recorrido = camino_recorrido[:S]
        tiempo_recorrido -= graph.dijkstra(camino_recorrido[-1], arrecife_a_visitar)[1]
        tiempo_total += tiempo_recorrido
        if camino_recorrido[-1] == arrecife_a_visitar:
            print(f"{' '.join(camino_recorrido)} HERMES LLEGA")
            arrecife_inicio = arrecife_a_visitar
            break
        print(f"{' '.join(camino_recorrido)} HERMES SE DUERME")
        arrecife_inicio = siguiente_letra(arrecifes, camino_recorrido[-1])
        S += 1

print(f"TIEMPO TOTAL: {tiempo_total}")

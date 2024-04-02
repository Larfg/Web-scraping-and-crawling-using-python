import heapq
class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()

    def add_edge(self, start_vertex, end_vertex):
        if start_vertex not in self.vertices:
            self.add_vertex(start_vertex)
        if end_vertex not in self.vertices:
            self.add_vertex(end_vertex)
        self.vertices[start_vertex].add(end_vertex)

    def get_neighbors(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]
        else:
            return set()


def dijkstra(graph, start, end):
    # Inicializar un diccionario para almacenar las distancias más cortas
    distances = {vertex: float('inf') for vertex in graph.vertices}
    distances[start] = 0

    # Inicializar un diccionario para almacenar los nodos previos en el camino más corto
    previous_vertices = {vertex: None for vertex in graph.vertices}

    # Inicializar una cola de prioridad (heap) para almacenar los nodos a explorar
    priority_queue = [(0, start)]

    while priority_queue:
        # Obtener el nodo con la distancia más corta desde el inicio
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Si ya hemos visitado este nodo, continuamos
        if current_distance > distances[current_vertex]:
            continue

        # Para cada vecino del nodo actual
        for neighbor in graph.get_neighbors(current_vertex):
            # Calcular la distancia desde el inicio hasta el vecino a través del nodo actual
            distance = current_distance + 1  # En este caso, como no tenemos pesos, simplemente incrementamos en 1

            # Si encontramos un camino más corto hacia el vecino, actualizamos las distancias y el nodo previo
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruir el camino más corto desde el inicio hasta el final
    path = []
    current_vertex = end
    while previous_vertices[current_vertex] is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.insert(0, start)

    # Devolver el camino más corto y su longitud
    return path, distances[end]
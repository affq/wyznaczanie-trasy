from collections import defaultdict
from klasy import PriorityQueue

def read_graph(filename):
    f = open(filename)
    g = defaultdict(list)

    for line in f:
        if not line.startswith('#'):
            e = [int(x) for x in line.split()]
            g[e[0]].append(e[1])
    return g

def read_graph_undirected(filename):
    f = open(filename)
    g = defaultdict(list)

    for line in f:
        if not line.startswith('#'):
            e = [int(x) for x in line.split()]
            g[e[0]].append(e[1])
            g[e[1]].append(e[0])
    return g

def retrieve_path(prev, a, b):
    path = [b]

    while b != a:
        b = prev[b]
        path.append(b)

    path.reverse()
    return path

def retrieve_path2(prev, a, b):
    if b not in prev:
        return []
    path =[]
    current = b
    
    while current != a:
        path.append(current)
        current = prev[current]
    
    path.append(a)
    path.reverse()
    return path

def bfs(graph, a, b):
    queue = []
    visited = set()
    prev = {}

    queue.append(a)
    visited.add(a)
    prev[a] = None

    while queue:
        u = queue.pop(0)

        if u == b:
            return retrieve_path(prev, a, b)

        for w in graph[u]:
            if w not in visited:
                queue.append(w)
                visited.add(w)
                prev[w] = u
        
    return None

# na podstawie https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra

def dijkstra(graph,start_id,end_id):
    frontier = PriorityQueue()
    frontier.put(start_id, 0)
    #print(f"frontier {frontier.get_elements()}")
    came_from = {}
    cost_so_far = {}
    came_from[start_id] = None
    cost_so_far[start_id] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == end_id:
            break
        
        for edge, w_node in graph.get_node_by_id(current).get_neighbours():
            w = w_node.id
            #print(f"Neighbor of {current}: {w}")
            new_cost = cost_so_far[current] + edge.cost_length()
            if w not in cost_so_far or new_cost < cost_so_far[w]:
                cost_so_far[w] = new_cost
                priority = new_cost
                frontier.put(w, priority)
                came_from[w] = current
    
    return came_from, cost_so_far

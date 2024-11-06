from collections import defaultdict

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

def extractmin(Q,d):    #zwraca wierzchołek w Q o najmniejszej wartości d
    min = float('inf')
    u = None
    for v in Q:
        if d[v] < min:
            min = d[v]
            u = v
    return u

def dijkstra(graph,start_id,end_id):
    S = set()   #wierzcholki juz przetworzone
    Q = set([start_id])  #wierzcholki do przetworzenia
    
    d = {node_id: float('inf') for node_id in graph.nodes}  #tymczasowa najkrotsza sciezka do wierzcholka
    p = {node_id: None for node_id in graph.nodes}  #poprzednik w tymczasowej sciezce
    
    d[start_id] = 0
    
    neighbor_count =0
    processed_nodes = 0
    
    while Q:
        u = extractmin(Q,d)
        Q.remove(u)
        
        if u == end_id:
            break
        
        
        for edge, w_node in graph.get_node_by_id(u).get_neighbours():
           w = w_node.id
           neighbor_count += 1
           if w in S:
               continue
           
           if d[w] > d[u] + edge.cost_length():
               d[w] = d[u] + edge.cost_length()
               p[w] = u
               
               if w not in Q:
                   Q.add(w)
        
        S.add(u)
        processed_nodes += 1
        
        path = retrieve_path(p, start_id, end_id)
        path_length = d[end_id]
        
        return path, path_length, neighbor_count, processed_nodes
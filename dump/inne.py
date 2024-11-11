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
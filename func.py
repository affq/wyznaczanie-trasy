from collections import defaultdict
from klasy import *


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


def heurystyka(start_id, end_id,option):
    start = (start_id.split(','))
    end = (end_id.split(','))
    euklides_distance = ((int(start[0]) - int(end[0]))*(int(start[0]) - int(end[0])) + (int(start[1]) - int(end[1]))*(int(start[1]) - int(end[1])))**0.5
    if option == 'distance':
        return euklides_distance
    else:
        speed_m_s = road_classes_speed['A'] * 1000 / 3600
        time = euklides_distance / speed_m_s
        return time
    
# na podstawie https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra
def a_star(graph, start_id, end_id,option):
    frontier = PriorityQueue()
    frontier.put(start_id, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_id] = None
    cost_so_far[start_id] = 0
    
    while not frontier.empty():
        current = frontier.get()
        print(current)
        
        if current == end_id:
            break
        
        for edge, w_node in graph.get_node_by_id(current).get_neighbours():
            w = w_node.id
            
            if option == 'distance':
                new_cost = cost_so_far[current] + edge.cost_length()
            else:
                new_cost = cost_so_far[current] + edge.cost_time()  
            
            if w not in cost_so_far or new_cost < cost_so_far[w]:
                cost_so_far[w] = new_cost
                
                if option == 'distance':
                    priority = new_cost + heurystyka(w, end_id,'distance')
                else:
                    priority = new_cost + heurystyka(w, end_id,'time')
                
                frontier.put(w, priority)
                came_from[w] = current
    
    return came_from, cost_so_far
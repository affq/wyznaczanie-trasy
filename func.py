import math

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Zwraca odległość między dwoma punktami (x1, y1) i (x2, y2).
    """
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

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

# na podstawie https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra

def dijkstra(graph,start_id,end_id):
    from klasy import PriorityQueue
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
    from klasy import road_classes_speed
    start = (start_id.split(','))
    end = (end_id.split(','))
    euklides_distance = distance(int(start[0]), int(start[1]), int(end[0]), int(end[1]))
    if option == 'distance':
        return euklides_distance
    else:
        speed_m_s = road_classes_speed['A'] * 1000 / 3600
        time = euklides_distance / speed_m_s
        return time
    
# na podstawie https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra
def a_star(graph, start_id, goal_id, option):
    start_node = graph.get_node_by_id(start_id)
    goal_node = graph.get_node_by_id(goal_id)
    
    if start_node is None or goal_node is None:
        raise ValueError("Początkowy lub końcowy węzeł nie istnieje w grafie.")
    
    from queue import PriorityQueue
    frontier = PriorityQueue()
    frontier.put((0, start_node))
    
    came_from = {start_id: None}
    cost_so_far = {start_id: 0}
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current.id == goal_id:
            break
        
        for edge, neighbor in current.get_neighbours():
            # Oblicz koszt przejścia do sąsiada
            if option == 'distance':
                new_cost = cost_so_far[current.id] + edge.cost_length()
            else:
                new_cost = cost_so_far[current.id] + edge.cost_time()
            
            # Jeśli nowy koszt jest niższy niż poprzednio zapisany, aktualizujemy koszty
            if neighbor.id not in cost_so_far or new_cost < cost_so_far[neighbor.id]:
                cost_so_far[neighbor.id] = new_cost
                priority = new_cost + heurystyka(neighbor.id, goal_id, option)
                frontier.put((priority, neighbor))
                came_from[neighbor.id] = current.id
    
    return came_from, cost_so_far
import math
from queue import PriorityQueue

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Zwraca odległość między dwoma punktami (x1, y1) i (x2, y2).
    """
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

def retrieve_path(prev, a, b):
    """
    Zwraca ścieżkę w postaci listy nodów od punktu A do punktu B.
    """
    if b not in prev:
        return []
    path = []
    current = b
    
    while current != a:
        path.append(current)
        current = prev[current]
    
    path.append(a)
    path.reverse()
    return path

def dijkstra(graph,start_id,end_id):
    frontier = PriorityQueue()
    frontier.put(start_id, 0)
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


def heurystyka(start_node, end_node, option):
    from klasy import road_classes_speed
    start = (start_node.x, start_node.y)
    end = (end_node.x, end_node.y)
    euklides_distance = distance(int(start[0]), int(start[1]), int(end[0]), int(end[1]))
    if option == 'distance':
        return euklides_distance
    else:
        speed_m_s = road_classes_speed['A'] * 1000 / 3600
        time = euklides_distance / speed_m_s
        return time

def a_star(graph, start_node, goal_node, option):
    if start_node is None or goal_node is None:
        raise ValueError("Początkowy lub końcowy węzeł nie istnieje w grafie.")
    
    frontier = PriorityQueue()
    frontier.put((0, start_node))
    
    came_from = {start_node.id: None}
    cost_so_far = {start_node.id: 0}
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current.id == goal_node.id:
            break
        
        for edge, neighbor in current.get_neighbours():
            if edge.direction == 0: # Droga jest przejezda w obu kierunkach
                go = True
            elif edge.direction == 1 and edge.from_node == current: # Droga jest przejezdna tylko w kierunku  from_node -> to_node
                go = True
            elif edge.direction == 2 and edge.to_node == current: # Droga jest przejezdna tylko w kierunku to_node -> from_node
                go = True
            else:
                go = False
                
            if go:
                if option == 'distance':
                    new_cost = cost_so_far[current.id] + edge.cost_length()
                else:
                    new_cost = cost_so_far[current.id] + edge.cost_time()
                
                if neighbor.id not in cost_so_far or new_cost < cost_so_far[neighbor.id]:
                    cost_so_far[neighbor.id] = new_cost
                    priority = new_cost + heurystyka(neighbor, goal_node, option)
                    frontier.put((priority, neighbor))
                    came_from[neighbor.id] = current.id
    
    return came_from, cost_so_far

def create_reachability_map(graph, start_node_id, max_time):
    """
    Tworzy mapę zasięgów, które można osiągnąć w określonym maksymalnym czasie z wybranego wierzchołka.
    
    :param graph: Graf, w którym znajdują się węzły i krawędzie.
    :param start_node_id: Identyfikator początkowego wierzchołka.
    :param max_time: Maksymalny czas, jaki możemy przeznaczyć na podróż (w sekundach).
    :return: Słownik z węzłami i czasem potrzebnym do dotarcia do nich, ograniczony do max_time.
    """
    frontier = PriorityQueue()
    frontier.put((0, start_node_id))
    time_to_reach = {start_node_id: 0}
    came_from = {start_node_id: None}
    
    while not frontier.empty():
        current_time, current_id = frontier.get()
        
        # Jeśli czas dotarcia do obecnego wierzchołka przekracza max_time, pomijamy go
        if current_time > max_time:
            continue
        
        current_node = graph.get_node_by_id(current_id)
        
        for edge, neighbor in current_node.get_neighbours():
            if edge.direction == 0:  # Droga jest przejezdna w obu kierunkach
                go = True
            elif edge.direction == 1 and edge.from_node == current_node:  # Kierunek from_node -> to_node
                go = True
            elif edge.direction == 2 and edge.to_node == current_node:  # Kierunek to_node -> from_node
                go = True
            else:
                go = False
            
            if go:
                travel_time = edge.cost_time()
                new_time = current_time + travel_time
                
                if neighbor.id not in time_to_reach or new_time < time_to_reach[neighbor.id]:
                    time_to_reach[neighbor.id] = new_time
                    frontier.put((new_time, neighbor.id))
                    came_from[neighbor.id] = current_id
    
    # Zwracamy tylko węzły, do których można dotrzeć w max_time
    reachable_nodes= {node_id: time for node_id, time in time_to_reach.items() if time <= max_time}
    return reachable_nodes, came_from

def create_shp_from_path(graf,path, output_folder, output_name, spatial_reference):
    import arcpy
    
    with arcpy.da.InsertCursor(f"{output_folder}/{output_name}", ["NR", "SHAPE@"]) as cursor:
        edges_list = []
        for i in range(len(path)-1):
            start_node = path[i] 
            end_node = path[i + 1] 
            found_edge = False
            
            for edge in graf.edges.values():
                if (edge.from_node.id == start_node and edge.to_node.id == end_node) or (edge.from_node.id == end_node and edge.to_node.id == start_node):
                    edges_list.append(edge)
                    found_edge = True
                    break
            if not found_edge:
                print(f"Nie znaleziono krawędzi między {start_node} i {end_node}")
                arcpy.AddMessage(f"Nie znaleziono krawędzi między {start_node} i {end_node}")
                break
            
        for i, edge in enumerate(edges_list):
            # print(edge)
            geometry = arcpy.FromWKT(edge.wkt)
            cursor.insertRow([i, geometry])

    arcpy.AddMessage("Wygenerowano plik SHP")
    
def add_shp_to_map(path):
    import arcpy
    aprx = arcpy.mp.ArcGISProject("CURRENT")  # Uzyskanie bieżącego projektu ArcGIS
    map_obj = aprx.listMaps()[0]  # Pobranie pierwszej mapy w projekcie
    map_obj.addDataFromPath(path)  # Dodanie wygenerowanej warstwy do mapy
    arcpy.AddMessage(f"Dodano plik SHP do mapy: {path}")
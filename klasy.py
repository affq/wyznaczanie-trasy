from typing import List, Dict

road_classes_speed = {
    "motorway": 1,
    "trunk": 2,
    "primary": 3,
    "secondary": 4,
    "tertiary": 5,
    "unclassified": 6,
    "residential": 7,
    "service": 8,
    "track": 9,
    "pedestrian": 10,
}

class Wierzcholek:
    def __init__ (self, id: str, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.edges = []

    def get_neighbours(self):
        neighbours = []
        for edge in self.edges:
            node = edge.get_end(self)
            neighbours.append((edge, node))
        return neighbours
        
class Krawedz:
    def __init__(self, id: str, from_node: Wierzcholek, to_node: Wierzcholek, length: float, road_class: str, direction: str):
        self.id = id
        self.from_node = from_node
        self.to_node = to_node
        self.length = length
        self.road_class_speed = road_classes_speed[road_class]
        self.direction = direction

    def get_end(self, node: Wierzcholek):
        if self.from_node == node:
            return self.to_node
        else:    
            return self.from_node
    
    def cost_length(self):
        return self.length
    
    def cost_time(self):
        return self.length / self.road_class_speed

class Graf:
    def __init__(self):
        self.edges = []
        self.nodes = []
    
    def add_edge(self, edge: Krawedz):
        self.edges.append(edge)

        if edge.from_node not in self.nodes:
            self.nodes.append(edge.from_node)
        else:
            edge.from_node.edges.append(edge)

        if edge.to_node not in self.nodes:
            self.nodes.append(edge.to_node)
        else:
            edge.to_node.edges.append(edge)
    
    def get_node_by_id(self, id: int):
        for node in self.nodes:
            if node.id == id:
                return node
        return None
    
    def get_edge_by_id(self, id: int):
        for edge in self.edges:
            if edge.id == id:
                return edge
        return None
    
    
        



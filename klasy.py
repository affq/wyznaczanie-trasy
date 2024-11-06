from typing import Dict, List
import heapq

road_classes_speed = {
    "A": 140,
    "S": 120,
    "GP": 100,
    "G": 80,
    "Z": 60,
    "L": 50,
    "D": 40,
    "I": 30
}

class Wierzcholek:
    def __init__(self, id: str, x: float, y: float):
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
    
    def __repr__(self):
        return f"Wierzcholek(id={self.id}, x={self.x}, y={self.y})"

class Krawedz:
    def __init__(self, id: int, from_node: Wierzcholek, to_node: Wierzcholek, length: float, road_class: str, direction: str):
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
        return self.length / (self.road_class_speed * 1000 / 3600) 
    
    def __repr__(self):
        return f"Krawedz(id={self.id}, from={self.from_node.id}, to={self.to_node.id}, length={self.length}, road_class={self.road_class_speed}, direction={self.direction})"

class Graf:
    def __init__(self):
        self.edges: Dict[str, Krawedz] = {}
        self.nodes: Dict[str, Wierzcholek] = {}

    def add_edge(self, edge: Krawedz):
        self.edges[edge.id] = edge

        self.nodes.setdefault(edge.from_node.id, edge.from_node).edges.append(edge)
        self.nodes.setdefault(edge.to_node.id, edge.to_node).edges.append(edge)

    def get_node_by_id(self, id: str) -> Wierzcholek:
        return self.nodes.get(id)

    def get_edge_by_id(self, id: str) -> Krawedz:
        return self.edges.get(id)


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
    def get_elements(self): 
        return self.elements
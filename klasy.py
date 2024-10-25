from typing import List

class Node:
    def __init__ (self, x: float, y: float, edges: List["Edge"]):
        self.x = x
        self.y = y
        self.edges = edges

class Edge:
    def __init__(self, from_node: "Node", to_node: "Node", cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

class Graf:
    def __init__(self, edges: List[Edge], nodes: List[Node]):
        self.edges = edges
        self.nodes = nodes
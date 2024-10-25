from typing import List, Dict

class Node:
    def __init__ (self, x: float, y: float, edges: List["Edge"]):
        self.x = x
        self.y = y
        self.edges = edges
        
# N1 = Node(1, 1, [Edge(None, None, 1)])
# N2 = Node(2, 2, [Edge(None, None, 1)])
# N3 = Node(3, 3, [Edge(None, None, 1)])
# N4 = Node(4, 4, [Edge(None, None, 1)])
# N5 = Node(5, 5, [Edge(None, None, 1)])
# N6 = Node(6, 6, [Edge(None, None, 1)])
# N7 = Node(7, 7, [Edge(None, None, 1)])

# {
#     N2: [(N3, 5), (N5, 4)],
#     N3: [(N2, 1), (N4, 2)],
# }

class Edge:
    def __init__(self, from_node: "Node", to_node: "Node", cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

class Graf:
    def __init__(self, edges: List[Edge], nodes: List[Node]):
        self.edges = edges
        self.nodes = nodes
    
    def add_edge(self, edge: Edge):
        self.edges.append(edge)

        if edge.from_node not in self.nodes:
            self.nodes.append(edge.from_node)
        if edge.to_node not in self.nodes:
            self.nodes.append(edge.to_node)
    
    def get_node_by_id(self, id: int):
        for node in self.nodes:
            if node.id == id:
                return node
        return None
    
    #na razie precies
    def get_node_by_xy(self, x: float, y: float):
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node
        return None
        



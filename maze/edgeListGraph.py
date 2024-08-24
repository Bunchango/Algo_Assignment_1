from typing import List
from maze.util import Coordinates
from maze.graph import Graph

class EdgeListGraph(Graph):
    """
    Represents an undirected graph using an edge list. 
    Each edge is stored as a tuple of two vertices (Coordinates) and a boolean indicating the presence of a wall.
    This implementation allows for the addition, removal, and querying of vertices and edges, as well as updating wall statuses between vertices.
    """

    def __init__(self):
        # List to store edges where each edge is represented as a tuple (vert1, vert2, wallStatus)
        self.edges: List[tuple[Coordinates, Coordinates, bool]] = []
        # Set to store unique vertices
        self.vertices: set[Coordinates] = set()


    def addVertex(self, label: Coordinates):
        """
        Adds a vertex to the graph.
        If the vertex already exists, this method does nothing.
        """
        self.vertices.add(label)


    def addVertices(self, vertLabels: List[Coordinates]):
        """
        Adds multiple vertices to the graph.
        Iterates through the list of vertices and adds each one individually.
        """
        for label in vertLabels:
            self.addVertex(label)


    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False) -> bool:
        """
        Adds an edge between two vertices.
        If either vertex does not exist in the graph, the edge is not added.
        If the edge already exists, it is not added again.
        The 'addWall' parameter determines the initial wall status of the edge.
        Returns True if the edge was added, False otherwise.
        """
        # Check if both vertices exist in the graph
        if not self.hasVertex(vert1) or not self.hasVertex(vert2):
            return False
        
        # Add the edge if it doesn't already exist
        if not self.hasEdge(vert1, vert2):
            self.edges.append((vert1, vert2, addWall))
            return True
        
        return False


    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        """
        Updates the wall status of an existing edge.
        If the edge exists, updates its wall status and returns True.
        Returns False if the edge does not exist.
        """
        for i, (v1, v2, _) in enumerate(self.edges):
            if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                # Update the wall status in the edge list
                self.edges[i] = (v1, v2, wallStatus)
                return True
            
        return False


    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """
        Removes an edge between two vertices.
        If the edge exists, it is removed and the method returns True.
        Returns False if the edge does not exist.
        """
        for i, (v1, v2, _) in enumerate(self.edges):
            if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                # Remove the edge from the list
                self.edges.pop(i)
                return True
            
        return False


    def hasVertex(self, label: Coordinates) -> bool:
        """
        Checks if a vertex exists in the graph.
        Returns True if the vertex exists, False otherwise.
        """
        return label in self.vertices


    def hasEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """
        Checks if an edge exists between two vertices.
        Returns True if the edge exists, False otherwise.
        """
        return any((v1 == vert1 and v2 == vert2) or (v2 == vert1 and v1 == vert2) for v1, v2, _ in self.edges)


    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """
        Retrieves the wall status of an edge between two vertices.
        Returns the wall status if the edge exists, otherwise returns False.
        """
        for v1, v2, wallStatus in self.edges:
            if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                return wallStatus
            
        return False


    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        """
        Returns a list of all vertices that are connected to the given vertex by an edge.
        """
        neighbours = []
        
        # Iterate through the edges to find all neighbours of the given vertex
        for v1, v2, _ in self.edges:
            # Check if the vertex is the same as the given vertex
            if v1 == label:
                neighbours.append(v2)
            elif v2 == label:
                neighbours.append(v1)
                
        return neighbours

from typing import List
from maze.util import Coordinates
from maze.graph import Graph

class IncMatGraph(Graph):
    """
    Represents an undirected graph using an incidence matrix.
    The incidence matrix tracks the connections between vertices (Coordinates) and edges.
    This implementation allows for the addition, removal, and querying of vertices and edges, as well as updating wall statuses between vertices.
    """

    def __init__(self):
        # Dictionary to store vertices with their index in the incidence matrix
        self.vertices: dict[Coordinates, int] = {}
        # List to store edges where each edge is represented as a tuple (vert1, vert2, wallStatus)
        self.edges: List[tuple[Coordinates, Coordinates, bool]] = []
        # Incidence matrix where each row corresponds to a vertex and each column corresponds to an edge
        self.incidence_mat: List[List[int]] = []


    def addVertex(self, label: Coordinates):
        """
        Adds a vertex to the graph.
        If the vertex already exists, this method does nothing.
        Updates the incidence matrix to reflect the new vertex.
        """
        if not self.hasVertex(label):
            # Assign a new index to the vertex and add a corresponding row to the incidence matrix
            self.vertices[label] = len(self.vertices)
            self.incidence_mat.append([0] * len(self.edges))


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
        If either vertex does not exist or if the edge already exists, the edge is not added.
        The 'addWall' parameter determines the initial wall status of the edge.
        Returns True if the edge was added, False otherwise.
        """
        # Check if both vertices exist in the graph
        if vert1 not in self.vertices or vert2 not in self.vertices:
            return False
        
        # Check if the edge already exists
        if self.hasEdge(vert1, vert2):
            return False
        
        # Add the edge to the list
        self.edges.append((vert1, vert2, addWall))
        
        # Update the incidence matrix with the new edge
        for row in self.incidence_mat:
            row.append(0)  # Add a new column for the new edge
        
        # Connect the vertices in the incidence matrix
        index = len(self.edges) - 1  # Index of the new edge
        self.incidence_mat[self.vertices[vert1]][index] = 1
        self.incidence_mat[self.vertices[vert2]][index] = 1
        
        # If successful, return True
        return True


    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        """
        Updates the wall status of an existing edge.
        If the edge exists, updates its wall status and returns True.
        Returns False if the edge does not exist.
        """
        # Find the edge and update its wall status
        for i, (v1, v2, _) in enumerate(self.edges):
            if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                self.edges[i] = (v1, v2, wallStatus)
                return True
            
        return False


    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """
        Removes an edge between two vertices.
        If the edge exists, it is removed, and the incidence matrix is updated accordingly.
        Returns True if the edge was removed, False otherwise.
        """
        # Find and remove the edge from the list
        for i, (v1, v2, _) in enumerate(self.edges):
            if (v1 == vert1 and v2 == vert2) or (v2 == vert1 and v1 == vert2):
                self.edges.pop(i)
                
                # Remove the corresponding column from the incidence matrix
                for row in self.incidence_mat:
                    row.pop(i)
                
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
        return any((v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1) for v1, v2, _ in self.edges)


    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """
        Retrieves the wall status of an edge between two vertices.
        Returns the wall status if the edge exists, otherwise returns False.
        """
        for v1, v2, status in self.edges:
            if (v1 == vert1 and v2 == vert2) or (v2 == vert1 and v1 == vert2):
                return status
        return False


    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        """
        Returns a list of all vertices that are connected to the given vertex by an edge.
        """
        neighbours = []
        
        if self.hasVertex(label):
            index = self.vertices[label]  # Get the vertex index
            
            # Iterate over the edges and find connected vertices
            for i, (v1, v2, _) in enumerate(self.edges):
                if self.incidence_mat[index][i] == 1:
                    # Avoid adding the vertex itself
                    if v1 == label:
                        neighbours.append(v2)
                    else:
                        neighbours.append(v1)
                        
        return neighbours

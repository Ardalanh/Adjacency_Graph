import heapq
import sys


class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.numConnections = 0

    def addNeighbor(self, ver1, weight=1):
        self.connectedTo[ver1] = weight
        self.numConnections += 1

    def removeNeighbor(self, ver1):
        if ver1 in self.connectedTo:
            del self.connectedTo[ver1]
            self.numConnections -= 1

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def __contains__(self, n):
        return n in self.connectedTo

    def __iter__(self):
        return iter(self.connectedTo.keys())

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, ver1):
        return self.connectedTo[ver1]


class Graph:
    def __init__(self):
        self.vertices = {}
        self.numVertices = 0
        self.numEdges = 0
        self.edgeList = []

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def getVertices(self):
        return self.vertices.keys()

    def __iter__(self):
        return iter(self.vertices.values())

    def __contains__(self, n):
        return n in self.vertices

    def __str__(self):
        res = "vertices: "
        for k in self.vertices:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edgeList:
            res += str(edge) + " "
        return res

    def addEdge(self, ver1, ver2, weight=1):
        if ver1 not in self.vertices:
            nv1 = self.addVertex(ver1)
        if ver2 not in self.vertices:
            nv2 = self.addVertex(ver2)

        self.numEdges += 1
        self.edgeList.append({self.vertices[ver1].id, self.vertices[ver2].id})

        self.vertices[ver1].addNeighbor(self.vertices[ver2], weight)
        self.vertices[ver2].addNeighbor(self.vertices[ver1], weight)

    def getEdgeWeight(self, ver1, ver2):
        return self.vertices[ver1].getWeight(self.vertices[ver2])

    def getEdges(self, ver1=None):
        if ver1:
            return [edge for edge in self.edgeList if ver1 in edge]
        else:
            return self.edgeList

    def removeEdge(self, ver1, ver2):
        self.numEdges -= 1
        self.vertices[ver1].removeNeighbor(self.vertices[ver2])
        self.vertices[ver2].removeNeighbor(self.vertices[ver1])

    def getVertexDegree(self, ver1):
        return self.vertices[ver1].numConnections

    def getDegrees(self):
        seq = []
        for vertex in self.vertices:
            seq.append(self.getVertexDegree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)

    def density(self):
        V = self.numVertices
        E = self.numEdges
        return 2.0 * E / (V * (V - 1))

    def brute_path(self, ver1, ver2, path=[]):
        path = path + [ver1]
        if ver1 == ver2:
            return path
        if ver1 not in self.vertices:
            return None
        for node in self.vertices[ver1]:
            if node.id not in path:
                newpath = self.brute_path(node.id, ver2, path)
                if newpath:
                    return newpath
        return None

    def brute_all_paths(self, ver1, ver2, path=[]):
        path = path + [ver1]
        if ver1 == ver2:
            return [path]
        if ver1 not in self.vertices:
            return []
        paths = []
        for node in self.vertices[ver1]:
            if node.id not in path:
                newpaths = self.brute_all_paths(node.id, ver2, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    
    def dijkstra(self, start, finish=None):
        distances = {} # Distance from start to node
        previous = {}  # Previous node in optimal path from source
        nodes = [] # Priority queue of all nodes in Graph
        
        
        for vertex in self.vertices:
            if vertex == start: # Set root node as distance of 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = 'Not Checked'

        while nodes:
            smallest = heapq.heappop(nodes)[1] # Vertex in nodes with smallest distance in distances
            if smallest == finish: # If the closest node is our target we're done so print the path
                path = []
                while not previous[smallest] == 'Not Checked': # Traverse through nodes til we reach the root which is 0
                    path.append(smallest)
                    smallest = previous[smallest]
                path.append(start)
                return path

            if distances[smallest] == sys.maxsize: # All remaining vertices are inaccessible from source
                break

            for neighbor in self.vertices[smallest]: # Look at all the nodes that this vertex is attached to
                alt = distances[smallest] + self.getEdgeWeight(smallest,neighbor.id) # Alternative path distance
                if alt < distances[neighbor.id]: # If there is a new shortest path update our priority queue (relax)
                    distances[neighbor.id] = alt
                    previous[neighbor.id] = smallest
                    for n in nodes:
                        if n[1] == neighbor.id:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
        return distances

    def brute_shortest_path(self, ver1, ver2, path=[]):
            path = path + [ver1]
            if ver1 == ver2:
                return path
            if ver1 not in self.vertices:
                return None
            shortest = None
            for node in self.vertices[ver1]:
                if node.id not in path:
                    newpath = self.brute_shortest_path(node.id, ver2, path)
                    if newpath:
                        if not shortest or (len(newpath) < len(shortest)):
                            shortest = newpath
            return shortest

if __name__ == '__main__':
    g = Graph()

    lst1 = [[28, 36], [0, 2], [3, 34], [29, 21], [37, 35], [28, 32], [0, 10], [37, 2], [4, 5], [13, 14], [34, 35], [27, 19], [28, 34], [30, 31], [18, 26], [0, 9], [7, 8], [18, 24], [18, 23], [0, 5], [16, 17], [29, 30], [10, 11], [0, 12], [15, 16], [0, 11], [0, 17], [18, 22], [23, 24], [0, 7], [35, 23], [22, 23], [1, 2], [0, 13], [18, 27], [25, 26], [32, 33], [28, 31], [24, 25], [28, 35], [21, 22], [4, 33], [28, 29], [36, 22], [18, 25], [37, 23], [18, 21], [5, 6], [19, 20], [0, 14], [35, 36], [9, 10], [0, 6], [20, 21], [0, 3], [33, 34], [14, 15], [28, 33], [11, 12], [12, 13], [17, 1], [18, 19], [36, 29], [0, 4], [0, 15], [0, 1], [18, 20], [2, 3], [0, 16], [8, 9], [0, 8], [26, 27], [28, 30], [3, 4], [31, 32], [6, 7], [37, 1], [37, 24], [35, 2]]
    # lst1 = [[0, 1], [0, 2], [0, 3], [1, 2], [2, 4], [4, 5], [5, 6], [3, 6]]
    for j, k in lst1:
        g.addEdge(j, k)
    print(g.dijkstra(0,28))

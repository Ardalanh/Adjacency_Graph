class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.numConnections = 0

    def addNeighbor(self, ver1, weight=0):
        self.connectedTo[ver1] = weight
        self.numConnections += 1

    def removeNeighbor(self, ver1, weight=0):
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
        self.vertList = {}
        self.numVertices = 0
        self.numEdges = 0
        self.edgeList = []

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def __contains__(self, n):
        return n in self.vertList
    
    def __str__(self):
        res = "vertices: "
        for k in self.vertList:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edgeList:
            res += str(edge) + " "
        return res

    def addEdge(self, ver1, ver2, weight=0):
        if ver1 not in self.vertList:
            nv1 = self.addVertex(ver1)
        if ver2 not in self.vertList:
            nv2 = self.addVertex(ver2)
        self.numEdges += 1
        self.edgeList.append({self.vertList[ver1].id, self.vertList[ver2].id})
        self.vertList[ver1].addNeighbor(self.vertList[ver2], weight)
        self.vertList[ver2].addNeighbor(self.vertList[ver1], weight)
    
    def getEdges(self, ver1=None):
        if ver1:
            return [edge for edge in self.edgeList if ver1 in edge]
        else:
            return  self.edgeList

    def removeEdge(self, ver1, ver2, weight=0):
        self.numEdges -= 1
        self.vertList[ver1].removeNeighbor(self.vertList[ver2], weight)
        self.vertList[ver2].removeNeighbor(self.vertList[ver1], weight)
    
    def getVertexDegree(self, ver1):
        return self.vertList[ver1].numConnections
        
    def getDegrees(self):
        seq = []
        for vertex in self.vertList:
            seq.append(self.getVertexDegree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)
        
    def density(self):
        V = self.numVertices
        E = self.numEdges
        return 2.0 * E / (V *(V - 1))
    
    def find_path(self, ver1, ver2, path=[]):
        path = path + [ver1]
        if ver1 == ver2:
            return path
        if ver1 not in self.vertList:
            return None
        for node in self.vertList[ver1]:
            if node.id not in path:
                newpath = self.find_path(node.id, ver2, path)
                if newpath:
                    return newpath
        return None

    def find_all_paths(self, ver1, ver2, path=[]):
        path = path + [ver1]
        if ver1 == ver2:
            return [path]
        if ver1 not in self.vertList:
            return []
        paths = []
        for node in self.vertList[ver1]:
            if node.id not in path:
                newpaths = self.find_all_paths(node.id, ver2, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_path(self, ver1, ver2, path=[]):
            path = path + [ver1]
            if ver1 == ver2:
                return path
            if ver1 not in self.vertList:
                return None
            shortest = None
            for node in self.vertList[ver1]:
                if node.id not in path:
                    newpath = self.find_shortest_path(node.id, ver2, path)
                    if newpath:
                        if not shortest or( len(newpath) < len(shortest)):
                            shortest = newpath
            return shortest


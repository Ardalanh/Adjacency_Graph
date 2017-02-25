class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, ver1, weight=0):
        self.connectedTo[ver1] = weight

    def removeNeighbor(self, ver1, weight=0):
        if ver1 in self.connectedTo:
            del self.connectedTo[ver1]

    def __str__(self):
        return str(self.id) +
        ' connectedTo: ' + str([x.id for x in self.connectedTo])

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

    def addEdge(self, ver1, ver2, weight=0):
        if ver1 not in self.vertList:
            self.addVertex(ver1)
        if ver2 not in self.vertList:
            self.addVertex(ver2)
        self.vertList[ver1].addNeighbor(self.vertList[ver2], weight)
        self.vertList[ver2].addNeighbor(self.vertList[ver1], weight)

    def removeEdge(self, ver1, ver2, weight=0):
        self.vertList[ver1].removeNeighbor(self.vertList[ver2], weight)
        self.vertList[ver2].removeNeighbor(self.vertList[ver1], weight)

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
                    newpath = self.find_path(node.id, ver2, path)
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest

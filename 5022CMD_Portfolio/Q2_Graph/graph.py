"""
graph.py
Generic UNWEIGHTED DIRECTED graph (adjacency-list representation).

The graph does not know anything about courses: vertices can be any
hashable object (str, int, tuple, ...), so the class is reusable.

For every vertex we keep TWO sets:
   _out[v] = vertices that v points TO        (outgoing edges  v -> x)
   _in[v]  = vertices that point TO v         (incoming edges  x -> v)
Keeping the incoming set makes listIncomingAdjacentVertex O(in-degree)
instead of scanning the whole graph (O(V + E)).
"""


class Graph:
    def __init__(self):
        self._out = {}
        self._in = {}

    # ----------------------- required methods ------------------------- #
    def addVertex(self, vertex):
        """Add a vertex. Returns False if it already exists. O(1)."""
        if vertex in self._out:
            return False
        self._out[vertex] = set()
        self._in[vertex] = set()
        return True

    def addEdge(self, from_vertex, to_vertex):
        """Add a directed edge from_vertex -> to_vertex. O(1)."""
        if from_vertex not in self._out or to_vertex not in self._out:
            raise KeyError("Both vertices must exist before adding an edge")
        if from_vertex == to_vertex:
            raise ValueError("Self-loops are not allowed")
        if to_vertex in self._out[from_vertex]:
            return False                    # edge already exists
        self._out[from_vertex].add(to_vertex)
        self._in[to_vertex].add(from_vertex)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        """All vertices u such that there is an edge u -> vertex."""
        self._check(vertex)
        return list(self._in[vertex])

    # ----------------------- extra methods ---------------------------- #
    def listOutgoingAdjacentVertex(self, vertex):
        """All vertices w such that there is an edge vertex -> w."""
        self._check(vertex)
        return list(self._out[vertex])

    def removeEdge(self, from_vertex, to_vertex):
        """Remove edge from_vertex -> to_vertex. Returns True if removed."""
        self._check(from_vertex)
        self._check(to_vertex)
        if to_vertex not in self._out[from_vertex]:
            return False
        self._out[from_vertex].discard(to_vertex)
        self._in[to_vertex].discard(from_vertex)
        return True

    def hasEdge(self, from_vertex, to_vertex):
        return from_vertex in self._out and to_vertex in self._out[from_vertex]

    def hasPath(self, start, goal):
        """Depth-first search: is goal reachable from start? O(V + E)."""
        stack, seen = [start], set()
        while stack:
            v = stack.pop()
            if v == goal:
                return True
            if v not in seen:
                seen.add(v)
                stack.extend(self._out.get(v, ()))
        return False

    def getVertices(self):
        return list(self._out)

    def containsVertex(self, vertex):
        return vertex in self._out

    def _check(self, vertex):
        if vertex not in self._out:
            raise KeyError(f"Vertex {vertex!r} not found")

    def __len__(self):
        return len(self._out)

import itertools
import dataclasses
import heapq
import sys
import unittest

from typing import Dict, List, Optional


@dataclasses.dataclass(frozen=True)
class Edge:
    origin: str
    dest: str
    weight: int


@dataclasses.dataclass(frozen=False)
class WeightedVertex:
    id: str
    weight: int = sys.maxsize  # for our purpose, this is effectively infinity.
    previous: Optional['WeightedVertex'] = None
    # Mapping the id of a neighbour node to its weight.
    neighbors: Dict[str, int] = dataclasses.field(default_factory=dict)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id, )


class Graph:
    def __init__(self, edges: List[Edge]) -> None:
        self.g: Dict[str, WeightedVertex] = {}

        for edge in edges:
            if edge.origin not in self.g:
                self.g[edge.origin] = WeightedVertex(
                    id=edge.origin,
                )
            if edge.dest not in self.g:
                self.g[edge.dest] = WeightedVertex(
                    id=edge.dest,
                )

        for edge in edges:
            # For undirected graph, must also create the reverse link.
            self.g[edge.origin].neighbors[edge.dest] = edge.weight

    def values(self) -> List[WeightedVertex]:
        return list(self.g.values())


def dijkstras(graph: Graph, source: str, sink: str) -> int:
    """
    Return the minimum distance/weight/cost to get from `source` node
    to the `dest` node.
    """
    source_node = None
    sink_node = None
    # Don't trust that the weight vertices have the correct
    # weights. Reset them to needed initial values.
    for weighted_v in graph.g.values():
        weighted_v.previous = weighted_v if weighted_v.id == source else None
        weighted_v.weight = 0 if weighted_v.id == source else sys.maxsize
        if weighted_v.id == source:
            source_node = weighted_v
        if weighted_v.id == sink:
            sink_node = weighted_v

    if not source_node:
        raise ValueError(f"'{source}' source node not available in graph.")
    if not sink_node:
        raise ValueError(f"'{sink}' destination node not available in graph.")

    priority_q = PriorityQueue()
    priority_q.add_task(source_node, priority=source_node.weight)

    while not priority_q.empty():
        curr: WeightedVertex = priority_q.pop_task()

        for neighbor_key in curr.neighbors:
            neighbor = graph.g[neighbor_key]
            edge_weight = curr.neighbors[neighbor_key]
            alternate_weight = curr.weight + edge_weight

            if alternate_weight < neighbor.weight:
                neighbor.weight = alternate_weight
                neighbor.previous = curr
                priority_q.add_task(neighbor, priority=neighbor.weight)

    return sink_node.weight


class PriorityQueue:
    REMOVED = "<removed-task>"  # placeholder for a removed task

    def __init__(self):
        self.pq = []  # heap-organized items
        # Mapping of tasks to entries. Helps with removal of heap items.
        self.entry_finder = {}
        # Unique sequence count. Used to ensure items of priority
        # are returned in insertion order.
        self.counter = itertools.count()
        self._size = 0

    def add_task(self, task, priority=0):
        """
        Add a new task or update the priority of an existing task.
        """
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)
        self._size += 1

    def remove_task(self, task):
        """
        Mark an existing task as REMOVED.  Raise KeyError if not found.
        """
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        self._size -= 1

    def pop_task(self):
        """
        Remove and return the lowest priority task. Raise KeyError if empty.
        """
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                self._size -= 1
                return task
        raise KeyError("pop from an empty priority queue")

    def empty(self):
        return self._size == 0


class TestDijkstras(unittest.TestCase):
    def test(self):
        edges = [
            Edge("a", "b", 7),
            Edge("a", "c", 9),
            Edge("a", "f", 14),
            Edge("b", "c", 10),
            Edge("b", "d", 15),
            Edge("c", "d", 11),
            Edge("c", "f", 2),
            Edge("d", "e", 6),
            Edge("e", "f", 9)
        ]
        graph = Graph(edges=edges)

        for c in "abcdef":
            self.assertEqual(
                0,
                dijkstras(graph, c, c)
            )

        self.assertEqual(
            26,
            dijkstras(graph, "a", "e")
        )
        self.assertEqual(
            9,
            dijkstras(graph, "e", "f")
        )
        self.assertEqual(
            11,
            dijkstras(graph, "a", "f")
        )


if __name__ == "__main__":
    unittest.main()

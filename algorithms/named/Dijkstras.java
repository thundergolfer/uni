package algorithms.named;

import java.util.*;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class Dijkstras {
    /**
     * One edge of the graph (only used by Graph constructor)
     */
    public static class Edge {

        public final String v1, v2;
        public final int dist;

        public Edge(String v1, String v2, int dist) {
            this.v1 = v1;
            this.v2 = v2;
            this.dist = dist;
        }

        @Override
        public String toString() {
            return "Edge{" +
                    "v1='" + v1 + '\'' +
                    ", v2='" + v2 + '\'' +
                    ", dist=" + dist +
                    '}';
        }
    }

    static class WeightedVertex {
        public String id;
        public int weight = Integer.MAX_VALUE;
        public WeightedVertex previous = null;
        public HashMap<String, Integer> neighbors;

        public WeightedVertex(String id) {
            this.id = id;
            this.neighbors = new HashMap<>();
        }

        @Override
        public String toString() {
            return "WeightedVertex{" +
                    "id=" + id +
                    ", weight=" + weight +
                    ", previous=" + previous +
                    ", neighbors=" + neighbors +
                    '}';
        }
    }

    static class Graph {
        private final HashMap<String, WeightedVertex> graph;
        public Graph(Edge[] edges) {
            graph = new HashMap<>(edges.length);

            // One pass to find all vertices.
            for (Edge e : edges) {
                if (!graph.containsKey(e.v1)) {
                    graph.put(e.v1, new WeightedVertex(e.v1));
                }
                if (!graph.containsKey(e.v2)) {
                    graph.put(e.v2, new WeightedVertex(e.v2));
                }
            }

            // Another pass to set neighboring vertices.
            for (Edge e : edges) {
                graph.get(e.v1).neighbors.put(graph.get(e.v2).id, e.dist);
                // graph.get(e.v2).neighbours.put(graph.get(e.v1), e.dist); // also do this for an undirected
            }
        }

        public boolean containsKey(String key) {
            return graph.containsKey(key);
        }

        public Collection<WeightedVertex> values() {
            return graph.values();
        }
    }

    /**
     * Return minimum distance from source to sink.
     */
    static int solve(Graph g, String source, String sink) {
        if (!g.containsKey(source)) {
            System.err.printf("Graph doesn't contain start vertex \"%s\"%n", source);
            return -1;
        }

        PriorityQueue<WeightedVertex> priorityQueue = new PriorityQueue<WeightedVertex>(
                Comparator.comparingInt(v -> v.weight)
        );

        WeightedVertex sinkVertex = null;
        for (WeightedVertex v : g.values()) {
            v.previous = v.id.equals(source) ? v : null;
            v.weight = v.id.equals(source) ? 0 : Integer.MAX_VALUE;
            if (v.id.equals(sink)) {
                sinkVertex = v;
            }
            priorityQueue.add(v);
        }

        if (sinkVertex == null) {
            System.err.printf("Graph doesn't contain sink vertex \"%s\"%n", sink);
            return -1;
        }

        WeightedVertex curr;
        WeightedVertex neighbor;
        while (!priorityQueue.isEmpty()) {
            curr = priorityQueue.poll();

            if (curr.weight == Integer.MAX_VALUE) {
                break; // we can ignore u (and any other remaining vertices) since they are unreachable
            }

            for (Map.Entry<String, Integer> a : curr.neighbors.entrySet()) {
                neighbor = g.graph.get(a.getKey()); // the neighbour in this iteration

                final int alternateWeight = curr.weight + a.getValue();
                // If true, shorter path to neighbour found
                if (alternateWeight < neighbor.weight) {
                    priorityQueue.remove(neighbor);
                    neighbor.weight = alternateWeight;
                    neighbor.previous = curr;
                    priorityQueue.add(neighbor); // Re-queue with new weight.
                }
            }
        }
        return sinkVertex.weight;
    }

    @Test
    public void test() {
        Dijkstras.Edge[] graphEdges = {
                // Distance from node "a" to node "b" is 7.
                // In the current Graph there is no way to move the other way (e,g, from "b" to "a"),
                // a new edge would be needed for that
                new Dijkstras.Edge("a", "b", 7),
                new Dijkstras.Edge("a", "c", 9),
                new Dijkstras.Edge("a", "f", 14),
                new Dijkstras.Edge("b", "c", 10),
                new Dijkstras.Edge("b", "d", 15),
                new Dijkstras.Edge("c", "d", 11),
                new Dijkstras.Edge("c", "f", 2),
                new Dijkstras.Edge("d", "e", 6),
                new Dijkstras.Edge("e", "f", 9)
        };
        Graph g = new Graph(graphEdges);

        int actual = Dijkstras.solve(g, "a", "e");
        assertEquals(26, actual);

        String vertices = "abcdef";
        String curr;
        for (int i = 0; i < vertices.length(); i++) {
            curr = String.valueOf(vertices.charAt(i));
            assertEquals(0, Dijkstras.solve(g, curr, curr));
        }


        actual = Dijkstras.solve(g, "e", "f");
        assertEquals(9,  actual);

        actual = Dijkstras.solve(g, "a", "f");
        assertEquals(11,  actual);
    }
}

package algorithms.named;

import org.junit.Test;

import java.util.*;
import java.util.Collections;
import java.util.LinkedList;

import static org.junit.Assert.assertEquals;

public class TopologicalSort {
    boolean[] discovered;

    public TopologicalSort() {}

    List<Integer> sort(DirectedGraph g) {
        // Textbook annoyingly starts vertex nums at 1.
        this.discovered = new boolean[g.numVertices+1];

        Deque<Integer> order = new LinkedList<>();

        for (int i = 1; i <= g.numVertices; i++) {
            if (!this.discovered[i]) {
                recurse(g, order, i);
            }
        }

        return new ArrayList<>(order);
    }

    void recurse(DirectedGraph g, Deque<Integer> order, int start) {
        this.discovered[start] = true;

        EdgeNode neighbour;
        for (neighbour = g.adjacencyList[start]; neighbour != null; neighbour = neighbour.next) {
            if (!discovered[neighbour.vertex]) {
                recurse(g, order, neighbour.vertex);
            }
        }
        processVertexLate(start, order);
    }

    void processVertexLate(int vertex, Deque<Integer> order) {
        order.push(vertex);
        System.out.printf("Processed %d (late)\n", vertex);
    }

    static class EdgeNode {
        int vertex; // Vertex at end of edge
        EdgeNode next; // next node in adjacency list

        EdgeNode(int vertex) {
            this.vertex = vertex;
            this.next = null;
        }
    }

    static class DirectedGraph {
        int numVertices;
        int numEdges;
        EdgeNode[] adjacencyList;

        private DirectedGraph(int numVertices) {
            this.numEdges = 0;
            this.numVertices = numVertices;
            this.adjacencyList = new EdgeNode[numVertices+1]; // Using 1-based numbering of vertices.
        }

        void insertEdge(int left, int right) {
            EdgeNode rightNode = new EdgeNode(right);
            rightNode.next = this.adjacencyList[left];
            this.adjacencyList[left] = rightNode; // insert at head.
            this.numEdges++;
        }

        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i <= this.numVertices; i++) {
                sb.append(i).append(": ");
                for (EdgeNode p = this.adjacencyList[i]; p != null; p = p.next) {
                    sb.append(p.vertex);
                    sb.append(' ');
                }
                sb.append('\n');
            }
            return sb.toString();
        }

        public static DirectedGraph fromStringRepresentation(String graphStr) {
            String[] lines = graphStr.lines().toArray(String[]::new);
            DirectedGraph g;

            if (lines.length == 0) return null;

            int numVertices = Integer.parseInt(lines[0].split(" ")[0]);
            g = new DirectedGraph(numVertices);

            for (int i = 1; i < lines.length; i++) {
                String[] parts = lines[i].split(" ");
                int left = Integer.parseInt(parts[0]);
                int right = Integer.parseInt(parts[1]);
                g.insertEdge(left, right);
            }

            return g;
        }
    }

    @Test
    public void testGraphToString() {
        String gString = "2\n" +
                "1 2\n";
        DirectedGraph g = DirectedGraph.fromStringRepresentation(gString);

        assertEquals("1: 2 \n2: \n", g.toString());
    }

    @Test
    public void testTopoSort() {
        String gString = "7\n" +
                "1 2\n" +
                "1 3\n" +
                "2 4\n" +
                "2 3\n" +
                "3 5\n" +
                "3 6\n" +
                "5 4\n" +
                "6 5\n" +
                "7 1\n" +
                "7 6\n";

        List<Integer> expected = new ArrayList<>(List.of(7, 1, 2, 3, 6, 5, 4));

        DirectedGraph g = DirectedGraph.fromStringRepresentation(gString);
        TopologicalSort topsort = new TopologicalSort();
        List<Integer> actual = topsort.sort(g);
        assertEquals(expected, actual);
    }
}

package algorithms.named;

import org.junit.Test;

import java.util.Queue;
import java.util.concurrent.LinkedBlockingDeque;

import static org.junit.Assert.*;

public class BFS {
    boolean[] processed; // which vertices have been processed.
    boolean[] discovered; // which vertices have been discovered.
    int[] parent;

    public BFS() {}

    void traverse(Graph g, int start) {
        // Textbook annoyingly starts vertex nums at 1
        this.processed = new boolean[g.numVertices+1];
        this.discovered = new boolean[g.numVertices+1];
        this.parent = new int[g.numVertices+1];

        Queue<Integer> queue = new LinkedBlockingDeque<>();
        int current;
        int successor;

        queue.add(start);

        while (!queue.isEmpty()) {
            current = queue.remove();
            processVertexEarly(current);
            processed[current] = true;

            EdgeNode n = g.edges[current];
            while (n != null) {
                successor = n.vertex;
                if ((!processed[successor]) || g.directed) {
                    processEdge(current, successor);
                }
                if (!discovered[successor]) {
                    queue.add(successor);
                    discovered[successor] = true;
                    parent[successor] = current;
                }
                n = n.next;
            }
            processVertexLate(current);
        }
    }

    void processVertexEarly(int v) {
        System.out.printf("Processed vertex %d (early)\n", v);
    }

    void processVertexLate(int v) {
        System.out.printf("Processed vertex %d (late)\n", v);
    }

    void processEdge(int v, int successor) {
        System.out.printf("Processed edge %d %d\n", v, successor);
    }


    /*
     Node for adjacency list impl
     */
    static class EdgeNode {
        int vertex; // adjacency info. 'who is at the end of this edge?'
        int weight; // edge weight, if any
        private EdgeNode next;  // next node in list

        EdgeNode(int right) {
            this.vertex = right;
            this.weight = 0;
            this.next = null;
        }

        void setNext(EdgeNode next) {
            this.next = next;
        }

        EdgeNode getNext() {
            return this.next;
        }
    }

    static class Graph {
        static int MAX_VERTICES = 20;

        boolean directed;  // is the graph directed?
        int numEdges;
        int numVertices;
        int degree[]; // degree of each vertex
        EdgeNode[] edges;

        // We represent a directed edge (x, y) by an EdgeNode y in x's
        // adjacency list.
        // An undirected graph will have two edges in the data structure,
        // an EdgeNode y in x's adjacency list and an EdgeNode x in y's.

        private Graph(boolean directed) {
            this.directed = directed;
            this.numEdges = 0;
            this.numVertices = 0;
            this.degree = new int[MAX_VERTICES];
            this.edges = new EdgeNode[MAX_VERTICES];
        }

        void insertEdge(int left, int right, boolean directed) {
            // If directed == false, left -> right and not right -> left
            EdgeNode leftNode = new EdgeNode(right);
            leftNode.setNext(this.edges[left]);
            this.edges[left] = leftNode; // insert at head.

            this.degree[left]++;

            if (!directed) {
                this.insertEdge(right, left, true);
            } else {
                this.numEdges++;
            }
        }

        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i <= this.numVertices; i++) {
                sb.append(i).append(": ");
                for (EdgeNode p = this.edges[i]; p != null; p = p.next) {
                    sb.append(p.vertex);
                    sb.append(' ');
                }
                sb.append('\n');
            }
            return sb.toString();
        }

        /*
         * This Java code is based on the C code in 'The Algorithm Design Manual'.
         * It uses a graph representation like this:
         * Line 1 is the number of vertices followed by ' ' followed by number of edges
         * Subsequent lines are 'x y' representing an edge.
         * If 5 is the number of vertices then the vertices present in edges are exactly:
         * 1, 2, 3, 4, 5.
         * For instance, you can't have 1, 2, 5, 10, 11.
         */
        public static Graph fromStringRepresentation(String graphStr, boolean directed) {
            String[] lines = graphStr.lines().toArray(String[]::new);
            Graph g = new Graph(directed);

            for (int i = 0; i < lines.length; i++) {
                String[] parts = lines[i].split(" ");

                // First line gives the number of vertices.
                if (i == 0) {
                    g.numVertices = Integer.parseInt(parts[0]);
                } else {
                    int left = Integer.parseInt(parts[0]);
                    int right = Integer.parseInt(parts[1]);
                    g.insertEdge(left, right, directed);
                }
            }

            return g;
        }
    }

    @Test
    public void testGraphToString() {
        String gString = "2\n" +
                "1 2\n";

        Graph g = Graph.fromStringRepresentation(gString, true);

        assertEquals("1: 2 \n2: \n", g.toString());
    }

    @Test
    public void testDFSSearch() {
        String gString = "8\n" +
                "1 2\n" +
                "1 7\n" +
                "1 8\n" +
                "2 3\n" +
                "2 5\n" +
                "2 7\n" +
                "3 4\n" +
                "3 5\n" +
                "4 5\n" +
                "5 6\n";

        Graph g = Graph.fromStringRepresentation(gString, false);
        BFS bfs = new BFS();
        bfs.traverse(g, 1);
    }
}

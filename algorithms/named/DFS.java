package algorithms.named;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class DFS {
    boolean[] processed; // which vertices have been processed.
    boolean[] discovered; // which vertices have been discovered.
    int[] entryTime; // track the 'time' of entry & exit to node.
    int[] exitTime; // track the 'time' of entry & exit to node.
    int[] parent;

    /*
     Node for adjacency list impl
     */
    static class EdgeNode {
        int vertex; // adjacency info. The id of the node at the 'end' of the edge.
        int weight; // optional weight for edge.
        EdgeNode next; // next node in adjacency list.

        EdgeNode(int endVertex) {
            this.vertex = endVertex;
            this.weight = 0; // Constructor used for unweighted graph.
            this.next = null;
        }
    }

    void traverseRecursively(Graph g, int start) {
        if (g.numVertices == 0) {
            return;
        }
        // Textbook annoyingly starts vertex nums at 1
        this.processed = new boolean[g.numVertices+1];
        this.discovered = new boolean[g.numVertices+1];
        this.entryTime = new int[g.numVertices+1];
        this.exitTime = new int[g.numVertices+1];
        this.parent = new int[g.numVertices+1];

        recurse(g, start, 0);
    }

    int recurse(Graph g, int current, int time) {
        this.discovered[current] = true;
        time = time + 1;
        this.entryTime[current] = time;
        processVertexEarly(current);

        EdgeNode neighbour = g.edges[current];

        while (neighbour != null) {
            if (!this.discovered[neighbour.vertex]) {
                this.parent[neighbour.vertex] = current;
                processEdge(current, neighbour.vertex);
                time = recurse(g, neighbour.vertex, time);
            } else if (
                    ((!this.processed[neighbour.vertex]) &&
                            (this.parent[current] != neighbour.vertex))
                    || g.directed
            ) {
                processEdge(current, neighbour.vertex);
            }
            neighbour = neighbour.next;
        }
        this.processed[current] = true;
        this.exitTime[current] = time;
        processVertexLate(current);
        return time;
    }

    void processVertexEarly(int vertex) {
        System.out.printf("Processed %d (early)\n", vertex);
        System.out.printf("Vertex %d entry time is %d\n", vertex, this.entryTime[vertex]);
    }

    void processVertexLate(int vertex) {
        System.out.printf("Processed %d (late)\n", vertex);
        System.out.printf("Vertex %d exit time is %d\n", vertex, this.exitTime[vertex]);
    }

    void processEdge(int v, int successor) {
        if (this.parent[successor] != v) {
            System.out.printf("Processed BACK edge %d %d\n", v, successor);
        } else {
            System.out.printf("Processed TREE edge %d %d\n", v, successor);
        }
    }

    static class Graph {
        static int MAX_VERTICES = 20;

        boolean directed;
        int numEdges;
        int numVertices;
        EdgeNode[] edges;

        // We represent a directed edge (x, y) by an EdgeNode y in x's
        // adjacency list.
        // An undirected graph will have two edges in the data structure,
        // an EdgeNode y in x's adjacency list and an EdgeNode x in y's.

        private Graph(boolean directed) {
            this.directed = directed;
            this.numEdges = 0;
            this.numVertices = 0;
            this.edges = new EdgeNode[MAX_VERTICES];
        }

        void insertEdge(int left, int right, boolean directed) {
            EdgeNode rightNode = new EdgeNode(right);
            rightNode.next = this.edges[left];
            this.edges[left] = rightNode; // insert new edge at head.

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
                for (DFS.EdgeNode p = this.edges[i]; p != null; p = p.next) {
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
            Graph g = new Graph(directed);
            String[] lines = graphStr.lines().toArray(String[]::new);

            for (int j = 0; j < lines.length; j++) {
                String[] parts = lines[j].split(" ");
                if (j == 0) {
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
        DFS dfs = new DFS();
        dfs.traverseRecursively(g, 1);
    }
}

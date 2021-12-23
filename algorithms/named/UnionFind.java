package algorithms.named;

public class UnionFind {
    private static int defaultMaxSize = 100;
    private int[] parents;
    private int[] sizes;
    private int n;  // Number of elems in set.

    public UnionFind() {
        this(defaultMaxSize);
    }

    public UnionFind(int setSize) {
        this.parents = new int[setSize+1];
        this.sizes = new int[setSize+1];
        this.n = setSize;

        for (int i = 1; i <= this.n; i++) {
            this.parents[i] = i;
            this.sizes[i] = 1;
        }
    }

    public int rootOf(int i) {
        if (i > this.n) {
            throw new IllegalArgumentException();
        }

        if (this.parents[i] == i) {
            return i;
        }
        return rootOf(this.parents[i]);
    }

    public void union(int left, int right) {
        int rootRight;
        int rootLeft;

        rootLeft = rootOf(left);
        rootRight = rootOf(right);

        if (rootLeft == rootRight) {
            return; // already connected!
        }

        // Connect the shorter subtree to the longer,
        // to minimize tree height.
        if (this.sizes[left] >= this.sizes[right]) {
            // Make right a subtree of left.
            this.sizes[left] = this.sizes[right] + this.sizes[left];
            this.parents[rootRight] = rootLeft;
        } else {
            // Make left a subtree of right.
            this.sizes[right] = this.sizes[right] + this.sizes[left];
            this.parents[rootLeft] = rootRight;
        }
    }

    public boolean isConnected(int left, int right) {
        int rootLeft = rootOf(left);
        int rootRight = rootOf(right);
        return (rootLeft == rootRight);
    }

    public void processEdges(int[][] edges) {
        int[] edge;
        for (int edgeIdx = 0; edgeIdx < edges.length; edgeIdx++) {
            edge = edges[edgeIdx];
            union(edge[0], edge[1]);
        }
    }
}

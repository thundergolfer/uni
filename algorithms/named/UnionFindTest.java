package algorithms.named;

import org.junit.Test;

import static org.junit.Assert.*;

public class UnionFindTest {
    @Test
    public void testEmpty() {
        UnionFind uf = new UnionFind(0);
        int[][] edges = new int[0][0];
        uf.processEdges(edges);
        assertThrows(IllegalArgumentException.class, () -> {
            uf.isConnected(0, 1);
        });
    }

    @Test
    public void testCorrectness() {
        int [][] edges = {{ 1, 0 }, { 0, 2 },
                { 5, 3 }, { 3, 4 },
                { 6, 7 }};

        UnionFind uf = new UnionFind(8);
        uf.processEdges(edges);
        assertTrue(uf.isConnected(1, 1));
        assertTrue(uf.isConnected(1, 0));
        assertTrue(uf.isConnected(5, 4));
    }
}

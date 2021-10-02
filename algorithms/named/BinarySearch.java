package algorithms.named;

import java.util.concurrent.ThreadLocalRandom;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

public class BinarySearch {
    private static <T extends Comparable<? super T>> boolean search(List<T> items, T target) {
        if (items.size() < 1) return false;
        int hi = items.size() - 1;
        int lo = 0;

        for (int mid = (hi + lo) / 2; lo <= hi; mid = (hi + lo) / 2) {
            T current = items.get(mid);
            if (current.compareTo(target) == 0) {
                return true;
            } else if (current.compareTo(target) > 0) {
                hi = mid - 1;
            } else {  // current < target
                lo = mid + 1;
            }
        }
        return false;
    }

    @Test
    public void testBinarySearch() {
        List<Integer> empty = new ArrayList<>();
        int randomNum = ThreadLocalRandom.current().nextInt(0, 1000001);
        assertFalse( "Searching empty list should always return false", search(empty, randomNum));
        assertFalse(search(new ArrayList<Integer>(List.of(1, 2, 3)), 4));
        assertTrue(search(new ArrayList<Integer>(List.of(1, 2, 3)), 3));
        assertTrue(search(new ArrayList<String>(List.of("apple", "bang", "cherry")), "cherry"));
    }
}

package algorithms.named;

import org.junit.Test;

import javax.annotation.processing.SupportedSourceVersion;
import java.util.Arrays;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertTrue;

/**
 * Page 129 in Skiena's *The Algorithm Design Manual*
 */
public class Mergesort {
    public void sort(int[] items) {
        sortPartition(items, 0, items.length-1);
    }

    /**
     * Sort is *inclusive* of `lo` and `hi`.
     */
    private void sortPartition(int[] items, int lo, int hi) {
        if (lo < hi) {
            int middle = (lo + hi) / 2;
            sortPartition(items, lo, middle);
            sortPartition(items, middle + 1, hi);

            merge(items, lo, middle, hi);
        }
    }

    /**
     * Merge is *inclusive* of `lo` and `hi`.
     */
    private void merge(int[] items, int lo, int middle, int hi) {
        int[] leftPartition = Arrays.copyOfRange(items, lo, middle+1); // middle+1 idx is excluded.
        int[] rightPartition = Arrays.copyOfRange(items, middle+1, hi+1); // hi+1 idx is excluded.

        int leftPointer = 0;
        int rightPointer = 0;
        int i;
        for (i = lo; leftPointer < leftPartition.length && rightPointer < rightPartition.length; i++) {
            if (leftPartition[leftPointer] <= rightPartition[rightPointer]) {
                items[i] = leftPartition[leftPointer];
                leftPointer++;
            } else {
                items[i] = rightPartition[rightPointer];
                rightPointer++;
            }
        }

        for (; leftPointer < leftPartition.length; leftPointer++, i++) {
            items[i] = leftPartition[leftPointer];
        }
        for (; rightPointer < rightPartition.length; rightPointer++, i++) {
            items[i] = rightPartition[rightPointer];
        }
    }

    @Test
    public void testEmpty() {
        Mergesort mergeSorter = new Mergesort();
        mergeSorter.sort(new int[0]);
    }

    @Test
    public void testCorrectness() {
        Mergesort mergeSorter = new Mergesort();
        int[] actual = new int[]{
          0, 1, 2, 3, 4
        };
        int[] expected = actual.clone();
        mergeSorter.sort(actual);
        assertArrayEquals(actual, expected);

        actual = new int[]{
                4, 3, 2, 1, 0
        };
        expected = new int[]{
                0, 1, 2, 3, 4
        };
        mergeSorter.sort(actual);
        assertArrayEquals(actual, expected);
    }
}

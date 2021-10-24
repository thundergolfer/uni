package books.data_science_from_scratch.linear_algebra; // Obviously not conventional casing

import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import static org.junit.Assert.*;

public class LinearAlgebra {
    static double[] add(double[] v, double[] w) {
        assert v.length == w.length : "vectors must be the same length";
        double[] result = new double[v.length];
        for (int i = 0; i < v.length; i++) {
            result[i] = v[i] + w[i];
        }
        return result;
    }

    static double[] subtract(double[] v, double[] w) {
        assert v.length == w.length : "vectors must be the same length";
        double[] result = new double[v.length];
        for (int i = 0; i < v.length; i++) {
            result[i] = v[i] - w[i];
        }
        return result;
    }

    /**
     * Componentwise sum a list of vectors.
     */
    static double[] vectorSum(List<double[]> vectors) {
        assert vectors.size() > 0 : "Must provide at least one vector";
        Set<Integer> lengths = vectors
                .stream()
                .map(elem -> elem.length)
                .collect(Collectors.toSet());
        assert (lengths.size() == 1) : "Vectors are not all the same length";

        int vectorLength = vectors.get(0).length;
        double[] result = new double[vectorLength];
        for (int i = 0; i < vectorLength; i++) {
            for (int j = 0; j < vectors.size(); j++) {
                result[i] += vectors.get(j)[i];
            }
        }
        return result;
    }

    /**
     * Multiplies every element by c.
     */
    static double[] scalarMultiply(double c, double[] v) {
        return Arrays.stream(v).map(elem -> c * elem).toArray();
    }

    /**
     * Computes the element-wise average.
     */
    static double[] vectorMean(List<double []> vectors) {
        double c = 1.0 / vectors.size();
        return scalarMultiply(c, vectorSum(vectors));
    }

    /**
     * Computes v_1 * w_1 + ... + v_n * w_n.
     */
    static double dot(double[] v, double[] w) {
        assert v.length == w.length : "vectors must be the same length";
        double result = 0;
        for (int i = 0; i < v.length; i++) {
            result += v[i] * w[i];
        }
        return result;
    }

    static double sumOfSquares(double[] v) {
        return dot(v, v);
    }

    /**
     * Returns the magnitude (or length) of vector v.
     */
    static double magnitude(double[] v) {
        return Math.sqrt(dot(v, v));
    }

    static double squaredDistance(double[] v, double[] w) {
        return sumOfSquares(subtract(v, w));
    }

    /**
     * Computes the distance between v and w.
     */
    static double distance(double[] v, double[] w) {
        return magnitude(subtract(v, w));
    }

    @Test
    public void testAdd() {
        double[] v = new double[]{0.1, 0.2, 0.3};
        double[] w = new double[]{0.1, 0.2, 0.3};
        double[] expected = new double[]{0.2, 0.4, 0.6};

        double[] result = add(v, w);
        assertArrayEquals(result, expected, 0.001);
    }

    @Test
    public void testSubtract() {
        double[] one = new double[]{1.0, 2.0, 3.0};
        double[] two = new double[]{10.0, 1.0, 5.0};
        double[] expected = new double[]{-9.0, 1.0, -2.0};
        assertArrayEquals(subtract(one, two), expected, 0.001);
    }

    @Test
    public void testVectorSum() {
        double[] v = new double[]{1.0, 1.0, 1.0};
        List<double[]> vectors = List.of(v, v, v, v, v);
        double[] expected = new double[]{5.0, 5.0, 5.0};
        assertArrayEquals(vectorSum(vectors), expected, 0.001);
    }

    @Test
    public void testScalarMultiply() {
        double[] expected = new double[]{0.2, 0.4, 0.8};
        assertArrayEquals(scalarMultiply(2.0, new double[]{0.1, 0.2, 0.4}), expected, 0.0001);
    }

    @Test
    public void testVectorMean() {
        double[] v = new double[]{1.0, 1.0, 1.0};
        List<double[]> vectors = List.of(v, v, v, v, v);
        assertArrayEquals(vectorMean(vectors), v, 0.001);
    }

    @Test
    public void testDot() {
        double[] one = new double[]{1.0, 2.0, 3.0};
        double[] two = new double[]{10.0, 1.0, 5.0};
        double expected = 10 + 2 + 15;

        assertEquals(dot(one, two), expected, 0.0001);
    }

    @Test
    public void testMagnitude() {
        assertEquals(magnitude(new double[]{3, 4}), 5, 0.001);
    }
}

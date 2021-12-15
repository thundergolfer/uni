package com.thundergolfer.uni.optimization.basic_neuralnet_lib_java;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.BlockJUnit4ClassRunner;
import org.tensorflow.ndarray.DoubleNdArray;
import org.tensorflow.ndarray.NdArrays;
import org.tensorflow.ndarray.Shape;

import static org.junit.Assert.*;

/**
 * Tensor implements a n-dimensional array.
 */
@RunWith(BlockJUnit4ClassRunner.class)
public class Tensor {
    public DoubleNdArray tensor;

    public Tensor() {
        tensor = NdArrays.ofDoubles(Shape.of(2, 3, 2));
        tensor.elements(0).forEach(matrix -> {
            assertEquals(2, matrix.rank());
            assertEquals(Shape.of(3, 2), matrix.shape());
            matrix
                    .set(NdArrays.vectorOf(1.0, 2.0), 0)
                    .set(NdArrays.vectorOf(3.0, -4.0), 1)
                    .set(NdArrays.vectorOf(-5.0, 6.0), 2);
        });
    }


    public static double sum(Tensor a, Tensor b) {
        // (coords, scalar)
        return 2.0;
    }

    public static Tensor pow(Tensor a, int power) {
        Tensor raised = new Tensor();
        raised.tensor = NdArrays.ofDoubles(a.tensor.shape());
        a.tensor.copyTo(raised.tensor);
        raised.tensor.scalars().forEachIndexed((coords, scalar) -> {
            scalar.setDouble(Math.pow(scalar.getDouble(), power));
        });
        return raised;
    }

    @Test
    public void testFoo() {
        Tensor a = new Tensor();
        Tensor c = Tensor.pow(a, 2);
        c.tensor.scalars().forEach(scalar ->
                assertTrue(scalar.getDouble() > 0)
        );
        assertEquals(1, 1);
    }
}

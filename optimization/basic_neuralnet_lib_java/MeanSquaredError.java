package com.thundergolfer.uni.optimization.basic_neuralnet_lib_java;

/**
 * Mean squared error (MSE), although we're faking MSE
 * and just doing total squared error.
 */
public class MeanSquaredError implements Loss {

    @Override
    public double loss(Tensor predicted, Tensor actual) {
        return 0;
    }

    @Override
    public Tensor grad(Tensor predicted, Tensor actual) {
        return null;
    }
}

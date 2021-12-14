package com.thundergolfer.uni.optimization.basic_neuralnet_lib_java;

/**
 * A loss functions measure how good predictions are.
 * Used to adjust parameters of a neural network.
 */
public interface Loss {
    double loss(Tensor predicted, Tensor actual);
    Tensor grad(Tensor predicted, Tensor actual);
}

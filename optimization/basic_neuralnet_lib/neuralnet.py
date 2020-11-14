from optimization.basic_neuralnet_lib.tensors import Tensor
from optimization.basic_neuralnet_lib.layers import Layer

from typing import Iterator, Sequence, Tuple


class NeuralNet:
    def __init__(self, layers: Sequence[Layer]) -> None:
        self.layers = layers

    def forward(self, inputs: Tensor) -> Tensor:
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, gradient: Tensor) -> Tensor:
        for layer in reversed(self.layers):
            grad = layer.backward(gradient)
        return grad

    def params_and_gradients(self) -> Iterator[Tuple[Tensor, Tensor]]:
        for layer in self.layers:
            for name, parameter in layer.params.items():
                gradient = layer.gradients[name]
                yield parameter, gradient


class Optimizer:
    def step(self, neural_net: NeuralNet) -> None:
        raise NotImplementedError


class StochasticGradientDescent(Optimizer):
    def __init__(self, learning_rate: float = 0.02) -> None:
        self.learning_rate = learning_rate

    def step(self, neural_net: NeuralNet) -> None:
        for parameter, gradient in neural_net.params_and_gradients():
            parameter -= self.learning_rate * gradient

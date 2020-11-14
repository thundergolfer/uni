import numpy as np
from typing import Callable, Dict

from optimization.basic_neuralnet_lib.tensors import Tensor


class Layer:
    def __init__(self) -> None:
        self.params: Dict[str, Tensor] = {}
        self.gradients: Dict[str, Tensor] = {}
        self.inputs: Tensor = None

    def forward(self, inputs: Tensor) -> Tensor:
        raise NotImplementedError

    def backward(self, gradient: Tensor) -> Tensor:
        raise NotImplementedError


class LinearLayer(Layer):
    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        # Inputs are (batch_size, input_size)
        # Outputs are (batch_size, output_size)
        self.params["w"] = np.random.randn(input_size, output_size)
        self.params["b"] = np.random.randn(output_size)

    def forward(self, inputs: Tensor) -> Tensor:
        """

        :param inputs:
        :return:
        """
        return inputs @ self.params["w"] + self.params["b"]

    def backward(self, gradient: Tensor) -> Tensor:
        """
        if y = f(x) and x = a * b + c
        then dy/da = f'(x) * b
        then dy/db = f'(x) * a
        and dy/dc = f'(x)

        if y = f(x) and x = a @ b + c
        then dy/da = f'(x) @ b.T
        then dy/db = a.T @ f'(x)
        and dy/dc = f'(x)

        :param gradient:
        :return:
        """
        self.gradients["b"] = np.sum(gradient, axis=0)
        self.gradients["w"] = self.inputs.T @ gradient
        return gradient @ self.params["w"].T

F = Callable[[Tensor], Tensor]


class Activation(Layer):
    """
    Applies a function element-wise to inputs.
    """
    def __init__(self, f: F, f_prime: F) -> None:
        super().__init__()
        self.f = f
        self.f_prime = f_prime

    def forward(self, inputs: Tensor) -> Tensor:
        self.inputs = inputs
        return self.f(inputs)

    def backward(self, gradient: Tensor) -> Tensor:
        # TODO(Jonathon): How exactly does this work?
        return self.f_prime(self.inputs) * gradient


def tanh(x: Tensor) -> Tensor:
    return np.tanh(x)


def tanh_prime(x: Tensor) -> Tensor:
    # https://socratic.org/questions/what-is-the-derivative-of-tanh-x
    y = tanh(x)
    return 1 - y ** 2


class Tanh(Activation):
    def __init__(self):
        super(Tanh, self).__init__(f=tanh, f_prime=tanh_prime())

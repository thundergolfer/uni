import numpy as np

from optimization.basic_neuralnet_lib.tensors import Tensor


class Loss:
    def loss(self, predicted: Tensor, actual: Tensor) -> float:
        raise NotImplementedError

    def gradient(self, predicted: Tensor, actual: Tensor) -> Tensor:
        raise NotImplementedError


class TotalSquaredError(Loss):
    @staticmethod
    def loss(predicted: Tensor, actual: Tensor) -> float:
        return sum((predicted - actual) ** 2)

    @staticmethod
    def gradient(predicted: Tensor, actual: Tensor) -> Tensor:
        return 2 * (predicted - actual)

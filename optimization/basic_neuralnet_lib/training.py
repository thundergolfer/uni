import numpy as np

from optimization.basic_neuralnet_lib import neuralnet
from optimization.basic_neuralnet_lib import tensors
from optimization.basic_neuralnet_lib import loss

from typing import Iterator, NamedTuple

DEFAULT_BATCH_SIZE = 32


def train(
    network: neuralnet.NeuralNet,
    inputs: tensors.Tensor,
    targets: tensors.Tensor,
    num_epochs: int,
    loss: loss.Loss = loss.TotalSquaredError(),
    optimizer: neuralnet.Optimizer = neuralnet.StochasticGradientDescent(),
):
    iterator = BatchIterator(batch_size=DEFAULT_BATCH_SIZE)
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for batch in iterator(inputs, targets):
            predicted = network.forward(batch.inputs)
            epoch_loss += loss.loss(predicted, batch.targets)
            gradient = loss.gradient(predicted, batch.targets)
            network.backward(gradient)
            optimizer.step(network)
        if epoch % 10 == 0:
            print(f"epoch: {epoch}, epoch_loss: {epoch_loss}")


class Batch(NamedTuple):
    inputs: tensors.Tensor
    targets: tensors.Tensor


class BatchIterator:
    def __init__(self, batch_size: int, shuffle: bool = True):
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __call__(self, inputs: tensors.Tensor, targets: tensors.Tensor) -> Iterator[Batch]:
        # TODO(Jonathon): Add full shuffling, not just shuffling around batches of `batch_size`
        batch_starts = np.arange(0, len(inputs), self.batch_size)
        if self.shuffle:
            np.random.shuffle(batch_starts) # Eg. 0, 20, 40, 60 ... -> 60, 20, 0, 40, ...
        for start in batch_starts:
            end = start + self.batch_size
            batch_inputs = inputs[start:end]
            batch_targets = targets[start:end]
            yield Batch(
                inputs=batch_inputs,
                targets=batch_targets
            )

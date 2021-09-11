"""
The model trainer uses email spam datasets to train models,
which are serialized as model artefacts to be loaded by the spam detection
server to drive the effectiveness of the spam detection API.
"""

from typing import Callable

Email = str
Prediction = float
SpamClassifier = Callable[[Email], Prediction]


if __name__ == "__main__":
    pass

import numpy as np


def rmspe(predictions, actual) -> float:
    return (np.mean(((predictions - actual) / actual) ** 2)) ** (1 / 2)

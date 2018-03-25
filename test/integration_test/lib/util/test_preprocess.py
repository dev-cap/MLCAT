from lib.util.preprocess import *
import numpy as np


def test_is_outlier():

    points1 = np.array([[100, 50, 10], [40, 50, 6]], np.int32)
    points2 = np.array([1], np.int32)
    assert is_outlier(points1, 3.5).any() != True
    assert is_outlier(points2, 3.5).any() != True

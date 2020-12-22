# Copyright IRT Antoine de Saint Exupéry et Université Paul Sabatier Toulouse III - All
# rights reserved. DEEL is a research program operated by IVADO, IRT Saint Exupéry,
# CRIAQ and ANITI - https://www.deel.ai/
# =====================================================================================

import torch.nn as nn
import torch
import numpy as np
from torch.nn import init
from deel.torchlip.utils import (
    bjorck_norm,
    frobenius_norm,
    lconv_norm,
)
from deel.torchlip.utils.lconv_norm import compute_lconv_coef
from deel.torchlip.normalizers import bjorck_normalization


def test_bjorck_norm():
    """
    test bjorck_norm hook implementation
    """
    m = nn.Linear(2, 2)
    init.orthogonal_(m.weight)
    w1 = bjorck_normalization(m.weight)
    bjorck_norm(m)
    x = torch.rand(2)
    m(x)
    w2 = m.weight
    np.testing.assert_array_equal(w1.data, w2.data)


def test_frobenius_norm():
    """
    test frobenius_norm hook implementation
    """
    m = nn.Linear(2, 2)
    init.uniform_(m.weight)
    w1 = m.weight / torch.norm(m.weight)
    frobenius_norm(m)
    x = torch.rand(2)
    m(x)
    w2 = m.weight
    np.testing.assert_array_equal(w1.data, w2.data)


def test_lconv_norm():
    """
    test lconv_norm hook implementation
    """
    m = nn.Conv2d(1, 2, kernel_size=(3, 3), stride=(1, 1))
    init.orthogonal_(m.weight)
    w1 = m.weight * compute_lconv_coef(m.kernel_size, (1, 1, 5, 5), m.stride)
    lconv_norm(m)
    x = torch.rand(1, 1, 5, 5)
    m(x)
    w2 = m.weight
    np.testing.assert_array_equal(w1.data, w2.data)


if __name__ == "__main__":
    test_bjorck_norm()
    test_frobenius_norm()
    test_lconv_norm()

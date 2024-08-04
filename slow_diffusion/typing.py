# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_typing.ipynb.

# %% auto 0
__all__ = ['InFeatureMapTensor', 'OutFeatureMapTensor', 'TimeStepTensor', 'TimeStepEmbeddingTensor']

# %% ../nbs/01_typing.ipynb 2
from typing import TypeAlias

from jaxtyping import Float, Int
from torch import Tensor

# %% ../nbs/01_typing.ipynb 3
InFeatureMapTensor: TypeAlias = Float[Tensor, "bs c_in h_in w_in"]
OutFeatureMapTensor: TypeAlias = Float[Tensor, "bs c_out h_out w_out"]
TimeStepTensor: TypeAlias = Float[Tensor, "bs"]  # from 0 to 1
TimeStepEmbeddingTensor: TypeAlias = Float[Tensor, "bs t"]
"""Placeholder for prediction, required to use Cog"""
from cog import BasePredictor
from typing import Any

class Predictor(BasePredictor):
    def setup(self):
        ...

    def predict(self) -> Any:
        ...
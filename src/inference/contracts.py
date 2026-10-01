"""Minimal interface; model-specific schemas await the actual training export."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelStatus:
    ready: bool
    message: str


@dataclass(frozen=True)
class SubmittedInput:
    """Uninterpreted upload, not a validated feature vector or sequence."""

    filename: str
    content: bytes


@dataclass(frozen=True)
class PredictionResult:
    """Presentation envelope only; output semantics must come from the model."""

    summary: str
    bundle_id: str


class InferenceError(RuntimeError):
    """An inference failure suitable for an actionable UI message."""


class ModelUnavailableError(InferenceError):
    """No verified model is connected."""


class InferenceService(Protocol):
    def status(self) -> ModelStatus: ...

    def predict(self, submitted: SubmittedInput) -> PredictionResult: ...

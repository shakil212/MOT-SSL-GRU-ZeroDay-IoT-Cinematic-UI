"""Unavailable implementation until the Colab export has been verified."""

from src.inference.contracts import (
    ModelStatus,
    ModelUnavailableError,
    PredictionResult,
    SubmittedInput,
)


class UnavailableInferenceService:
    def status(self) -> ModelStatus:
        return ModelStatus(ready=False, message="Model not connected")

    def predict(self, submitted: SubmittedInput) -> PredictionResult:
        raise ModelUnavailableError(
            "Model not connected. A verified Colab export is required before prediction."
        )

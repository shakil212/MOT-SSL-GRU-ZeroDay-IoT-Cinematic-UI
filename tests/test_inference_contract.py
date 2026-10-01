import pytest

from src.inference.contracts import ModelUnavailableError, SubmittedInput
from src.inference.service import UnavailableInferenceService


@pytest.mark.parametrize("content", [b"", b"arbitrary input"])
def test_no_prediction_can_be_generated_without_a_model(content):
    service = UnavailableInferenceService()
    assert not service.status().ready
    with pytest.raises(ModelUnavailableError, match="Model not connected"):
        service.predict(SubmittedInput("input.txt", content))

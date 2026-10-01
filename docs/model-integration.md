# Model integration contract

## Current state

The app uses `UnavailableInferenceService`. Its status is unavailable and every prediction call raises `ModelUnavailableError`. No framework or artifact is loaded. The uploader is a demonstration file inspector, not a declaration of supported model inputs.

## Boundary

`Streamlit UI → InferenceService → future model adapter → verified artifact bundle`

`SubmittedInput` carries an uninterpreted filename and bytes. `ModelStatus` supplies readiness and an explanatory message. `PredictionResult` reserves a summary and bundle identifier without assuming classes or numerical scores. `InferenceError` is the base for actionable inference errors. Extend these contracts only when real output semantics are known; confidence/probability has deliberately not been invented.

## Integration sequence

1. Review the actual notebook and strict LOAFO protocol. Record dataset provenance, held-out attack family, fold identity, and leakage controls from the implementation.
2. Document accepted formats, exact feature order/types, missing-value handling, sequence construction, temporal ordering, preprocessing, framework versions, output interpretation, and any thresholds, using notebook evidence.
3. Export the actual model and required companion files into an immutable bundle. Record checksums and provenance in its manifest; preserve fold-specific artifacts.
4. Implement an adapter inside `src/inference/`. It loads only verified local artifacts, validates actual model inputs, applies the exact exported preprocessing, and returns documented outputs. Never load an uploaded model or deserialize user data as a model object.
5. Keep status unavailable for missing or incompatible bundles and give actionable errors. Cache verified model resources only; keep per-user input and results out of shared caches.
6. Replace the service construction in `app.py`, wire prediction only after readiness and actual input validation, and render results from the service. Invalidate old results when the input or selected bundle changes.
7. Compare local outputs with Colab reference outputs under an agreed numerical tolerance. Test supported and invalid inputs, missing/corrupt/incompatible artifacts, and fold provenance before enabling inference.

Only expose confidence/probability if the trained pipeline defines it. Document its meaning and range; never relabel an arbitrary score as probability. UI prediction results are separate from research evaluation metrics.

## Documentation destinations

- `docs/screenshots/`: reviewed screenshots of the running interface.
- `assets/`: graphics used by the application.
- `research/results/`: verified tables/figures with notebook revision, bundle ID, fold, configuration, and evaluation provenance.
- `research/presentations/`: slide source and selected final exports.

Create these directories when content exists; Git does not track empty directories.

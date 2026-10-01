# MOT-SSL-GRU-ZeroDay-IoT

University Machine Learning research demonstrator for zero-day IoT intrusion detection using temporal/self-supervised GRU-based learning and strict Leave-One-Attack-Family-Out (LOAFO) evaluation.

**Current stage: UI demonstration. Model not connected.** Training is maintained separately in Google Colab in `ZeroDay_IoT_Final_Training.ipynb`; the notebook and trained exports have not been supplied. This app does not generate predictions, confidence values, classes, or evaluation metrics.

## Cinematic UI preview

This worktree contains the dark research interface: a cyan/amber visual system, a static research-system graphic, three-stage overview cards, session-only submission and inspection, a truthful pipeline panel, and research provenance cards. Prediction remains disabled.

The main directory was used only as a read-only source for the initial application snapshot. No model, dataset, environment, credential, or Git metadata was copied into this preview.

Reusable presentation components live in `src/ui/components.py`; `src/ui/theme.css` owns visual tokens and scoped styles. Native theme colors come from `.streamlit/config.toml` through `src/ui/styles.py`. No external fonts, JavaScript, or frontend dependencies were added.

Inspection status distinguishes file receipt from readable text. Preprocessing, model execution, and prediction always remain pending. Filename extensions are descriptive metadata, not validated input formats.

## Run locally

Development environment: Windows, Python 3.14.0. Runtime and test dependencies are pinned separately; a training framework is not needed.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

Open `http://localhost:8502`. The stable application can remain on port 8501; run the command above from this preview workspace. For runtime-only installation, use `requirements.txt`. On macOS/Linux, substitute `.venv/bin/python` for the Windows interpreter path. Other operating systems have not been tested.

The presentation configuration uses Streamlit's viewer toolbar mode. To restore developer controls locally, append `--client.toolbarMode developer` to the launch command. Restart an already-running server after configuration changes.

## Demonstration walkthrough

1. Open **Overview** for the project context and model connection status.
2. Select **Open data submission** or use the sidebar, then choose a local file (maximum 10 MiB).
3. Inspect its filename, size, and first 8 KiB of UTF-8 text when readable. Empty, binary, and unreadable files produce explanatory messages. This preview does not establish model compatibility or validate features.
4. Observe that **Run prediction** is disabled and the prediction area reports **No prediction available — Model not connected**.
5. Open **Research notes** for the stated approach and pending integration information.

Uploads remain in Streamlit session memory; the app does not write them to disk or cache them globally. The selected file and preview survive navigation between all three pages. **Replace file** opens a new chooser while retaining the current selection; **Cancel replacement** keeps it. **Clear file** removes the selection. A new browser session or reload may reset the selection. No uploaded models are executed or deserialized.

The preview uses a 280-pixel scroll area with wrapped lines. Whitespace-only previews have an explicit empty state. Receipt and previewing of a file never imply that it is valid model input.

## Repository map

| Location | Responsibility |
| --- | --- |
| `app.py` | Entry point and navigation |
| `src/ui/` | Presentation, consistent styling, bounded file inspection, and session-only upload state |
| `src/inference/` | Framework-independent contracts and unavailable service |
| `.streamlit/config.toml` | Theme and upload limit |
| `artifacts/` | Ignored local model bundles; tracked storage guidance |
| `data/` | Ignored local data; tracked handling guidance |
| `notebooks/` | Future sanitized reference training notebook |
| `docs/model-integration.md` | Integration checklist and interface responsibilities |
| `tests/` | Model-unavailable behavior, file inspection, and app navigation checks |

Create `assets/`, `docs/screenshots/`, `research/results/`, and `research/presentations/` when their content is available. Store only verified research results with experiment provenance. Do not present runtime predictions as evaluation metrics.

## Model integration

The intended flow is **UI → inference service → model adapter → exported artifacts**. The UI never imports a training framework. Follow [the integration guide](docs/model-integration.md) before adding a real adapter or enabling prediction. Supported formats, feature schemas, sequences, preprocessing, prediction classes, and score semantics remain pending notebook review.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
```

UI tests use [Streamlit's AppTest API](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest). They exercise launch and navigation without model artifacts. File inspection tests cover unreadable data, size limits, and UTF-8 preview boundaries. These are application checks, not scientific validation of a trained model.

Interaction tests also cover upload retention, replacement cancellation, same-name replacement, clearing, and isolation between sessions. Upload persistence follows [Streamlit's widget-state guidance](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior): a separate session value holds the file independently of the temporary uploader widget.

All 24 automated checks pass in the redesign worktree. Browser-based visual verification remains pending because the browser connector and Windows computer-use helper were unavailable during implementation. See [UI review and presentation guide](docs/ui-review.md) for verified checks, outstanding viewport/accessibility checks, and presentation timing.

## Version control

The adjacent stable project is committed as `302b615` (`Baseline stable Streamlit UI before cinematic redesign`). Its working tree was verified clean after implementation. Redesign files remain uncommitted in this dedicated preview worktree.

`.gitignore` excludes environments, caches, credentials, local data, model bundles, checkpoints, and temporary outputs. Artifact/data guidance READMEs are retained. Review and sanitize any notebook or sample before committing. Keep model binaries in approved external storage or evaluate Git LFS when actual exports exist.

Requirements pin direct dependencies, not the full transitive environment. Review dependency changes in Git and rerun checks when upgrading. Add model-framework dependencies only after verifying compatibility with Colab exports.

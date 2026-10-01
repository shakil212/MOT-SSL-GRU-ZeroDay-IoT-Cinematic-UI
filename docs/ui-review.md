# UI review and presentation guide

## Implemented design

The interface uses a near-black canvas, layered blue-black cards, cyan actions, amber integration status, and a subtle CSS grid with radial glows. Typography, spacing, colors, borders, radii, and motion share semantic tokens. The research-system geometry is static decoration, hidden from assistive technology; it is not a visualization of live model activity.

- **Overview:** project hero, clearly identified research-direction chips, direct submission action, and Submit / Inspect / locked Predict cards.
- **Data submission:** native drag/drop uploader, file-received state, replacement/cancellation/clearing, bounded text inspection, a five-stage pipeline, and an intentional empty results panel.
- **Research notes:** stated methodology, planned LOAFO evaluation, separate training/integration status, notebook availability, and pending experiment provenance. The workflow is explicitly proposed, not a verified executable pipeline.
- **Sidebar:** original navigation labels and session key, selected-page styling, project identity, and compact model-unavailable status.

The interface never presents accuracy, predictions, confidence, feature definitions, dataset statistics, or experimental results. No model/framework is loaded. Inference contracts, session callbacks, the UTF-8 inspector, dependency pins, and inference-contract tests are unchanged from the copied baseline.

## Upload and pipeline semantics

Uploads remain in per-session memory. Replacement keeps the current file until another upload arrives; cancellation retains it. Clearing removes the selection. Navigation retains both the selection and replacement state. A reload/new browser session may reset them.

| Stage | Displayed state |
| --- | --- |
| Input | Awaiting file / File received |
| Inspection | Awaiting file / Preview available / No visible text / Preview unavailable |
| Preprocessing | Pending integration |
| Model | Model not connected |
| Prediction | Locked; Run prediction remains disabled |

Receipt and text inspection never mean that a file is valid model input. The existing inspector is evaluated once per submission-page render and its outcome is shared by the preview and pipeline. Truncated previews explicitly cover only the first 8 KiB. The preview remains 280px high with wrapped lines. Empty, whitespace-only, binary, unreadable, and oversized input retain explanatory states. The upload limit remains 10 MiB. Filename extension is metadata only; MIME type is not invented.

## CSS and maintenance

- `.streamlit/config.toml` configures native theme colors, typography, sidebar, borders, and radii.
- `src/ui/styles.py` reads native palette values and injects `src/ui/theme.css`; dynamic uploaded text never enters CSS or raw HTML.
- Custom markup uses `research-*` classes. Native container keys supply `st-key-research-*` scoping.
- The stylesheet ends with a **compatibility adapters** section for native radio labels, uploader drop zone, captions, focus, and responsive column layout. It uses semantic attributes and narrowly scoped Streamlit test IDs, never generated classes or positional selectors.
- Streamlit 1.64.0 wraps horizontal rows in `stLayoutWrapper`; responsive selectors account for that wrapper. This structure was checked against the installed frontend source, but still needs rendered-browser verification.
- The content cap is 1240px, with a 260px initial sidebar. Hero/submission columns stack below 1100px; workflow/research cards stack below 700px. Native sidebar controls remain available.
- Transitions are 200ms. Workflow-card hover lift is limited to 2px. Reduced-motion preferences remove transitions and lift. There is no continuous animation or backdrop-blur dependency.

Retest these adapters after a Streamlit upgrade. Favor native accessibility and functionality over exact cosmetic parity if widget internals change. Viewer toolbar mode retains ordinary viewer controls. Restart the server after native configuration changes.

## Verification on 2026-10-01

Completed:

- All **16 baseline tests** passed after source copying.
- All **24 tests** pass after redesign, including seven pipeline-state cases and a replacement/cancel/clear pipeline lifecycle check.
- Existing checks retain upload persistence, cancellation, same-name replacement, session isolation, long filenames, Unicode boundaries, bounded previews, and disabled prediction.
- Dependency consistency check: `pip check` passed.
- Follow-up full suite: **24 passed in 5.87s**, with pytest cache and bytecode writes disabled for that run. Original baseline behavior remains covered; no tests were weakened.
- Explicit imports of the UI components, styles, session module, inference contracts, and inference service passed and resolved to this preview workspace.
- Python compilation of `app.py`, `src`, and `tests` passed. Installed versions match the pins: Streamlit **1.64.0**, pytest **9.1.1**, on Python **3.14.0**.
- Local Streamlit startup and `/_stcore/health` check passed on port 8502.
- The existing preview server remained healthy during follow-up verification; HTTP health returned `ok`. The stable project is at commit `302b615` and its working tree was verified clean using read-only Git commands with optional locks disabled.
- Byte comparisons confirm unchanged session/inference modules, dependency pins, and inference-contract tests. AST comparison confirms the inspector is unchanged.
- Calculated minimum text contrast against the three solid backgrounds: primary 15.31:1, secondary 9.87:1, muted 6.65:1, cyan 9.52:1, blue 7.54:1, amber 9.35:1, success 10.23:1, error 7.97:1. These calculations do not verify actual composited surfaces, native disabled controls, or browser-rendered colors.

**Visual verification is pending.** Browser discovery returned no available browser surfaces; opening Chrome reported `Browser is not available: chrome`. The Windows computer-use helper reported an unavailable native pipe. No rendered screenshots or browser/accessibility claims have been recorded. No screenshot directory was created without actual screenshots.

Follow-up browser discovery again returned no apps or browsers. Accordingly, the manual checklist below remains required rather than being marked passed.

| Pending check | Acceptance criteria |
| --- | --- |
| 1920×1080, 1440×900, 1366×768 | Three pages readable, desktop columns balanced, model status easy to locate |
| 820px tablet width | Hero/submission panels stack; upload and inspection precede pipeline/results |
| 390px narrow width | Single-column cards, accessible navigation, no page-level horizontal scrolling |
| 200% browser zoom | No overlapping labels, clipped controls, or unreadable filenames |
| Keyboard | Tab/Shift+Tab focus visible; radio arrows, upload actions, and expanders usable |
| Screen reader | Meaningful headings, file states, warnings, and disabled prediction; decoration ignored |
| Rendered contrast | Normal text at least 4.5:1, large text 3:1; focus and status distinguishable |
| Reduced motion | Hover lift and transitions absent when reduced motion is enabled |
| Long content | Filename wraps; preview remains bounded; no implication that the whole file was inspected |
| Projector | Dark surfaces remain distinguishable; body text and amber/cyan status readable |

After browser verification, save actual screenshots under `docs/screenshots/`: `overview.png`, `submission-empty.png`, `submission-readable.png`, `submission-unavailable.png`, `research-notes.png`, and `submission-narrow.png`. Use only non-sensitive inspection text; never label it as model-ready data.

## Implementation file inventory

The initial preview baseline copied exactly **21 source/configuration/documentation files** from the stable project. The preview already contained the redesign when the follow-up approval arrived, so no baseline files were recopied or overwritten.

| Copied group | Files |
| --- | --- |
| Project root | `.gitignore`, `app.py`, `README.md`, `requirements.txt`, `requirements-dev.txt` |
| Configuration | `.streamlit/config.toml` |
| UI source | `src/__init__.py`, `src/ui/__init__.py`, `src/ui/components.py`, `src/ui/session.py`, `src/ui/styles.py` |
| Inference source | `src/inference/__init__.py`, `src/inference/contracts.py`, `src/inference/service.py` |
| Tests | `tests/test_ui.py`, `tests/test_inference_contract.py` |
| Documentation | `docs/model-integration.md`, `docs/ui-review.md`, `artifacts/README.md`, `data/README.md`, `notebooks/README.md` |

New application file: `src/ui/theme.css`.

Modified relative to the copied baseline: `.streamlit/config.toml`, `app.py`, `src/ui/components.py`, `src/ui/styles.py`, `tests/test_ui.py`, `README.md`, and `docs/ui-review.md`. The follow-up pass only changed the two documentation files to make port 8502 the primary preview command and record verification/inventory details.

No Git metadata, environment, credentials, secrets, datasets, uploaded data, model binaries, temporary files, or pre-existing caches were copied. Verification may generate ignored Python/pytest caches within the preview workspace. Existing installed dependencies were reused without installation or modification.

## Local verification and presentation

```powershell
python -m pytest -q
python -m pip check
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8502
```

Use an environment installed from `requirements-dev.txt`. The preview server uses a separate port from the stable app. To enable developer toolbar options, append `--client.toolbarMode developer`.

| Time | Presenter focus |
| --- | --- |
| 0:00–1:30 | Research problem, stated approach, and model-pending status |
| 1:30–3:00 | Research notes: planned LOAFO protocol and missing reference artifacts |
| 3:00–5:30 | File submission, bounded inspection, navigation retention, replacement/cancellation |
| 5:30–6:30 | Truthful pipeline states and disabled prediction |
| 6:30–8:00 | Implemented interface and next steps toward verified integration |

Rehearse on the actual display. Clear the selected file before a new demonstration. The interface demonstrates inspection, not scientific validation of a trained model.

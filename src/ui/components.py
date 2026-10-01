"""Reusable interface pieces and bounded, non-model file inspection."""

import codecs
from dataclasses import dataclass
from html import escape
from pathlib import PurePath
from typing import Literal

import streamlit as st

from src.inference.contracts import ModelStatus, SubmittedInput
from src.ui.session import cancel_replacement, clear_file, receive_upload, replace_file

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
PREVIEW_BYTES = 8 * 1024


def text_preview(content: bytes) -> tuple[str, bool]:
    """Inspect a UTF-8 prefix without interpreting columns or model features."""
    if not content:
        raise ValueError("The file is empty. Choose a non-empty file to inspect.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("This demonstration accepts files up to 10 MiB.")
    truncated = len(content) > PREVIEW_BYTES
    decoder = codecs.getincrementaldecoder("utf-8-sig")()
    try:
        preview = decoder.decode(content[:PREVIEW_BYTES], final=not truncated)
    except UnicodeDecodeError as exc:
        raise ValueError(
            "A text preview is unavailable: this file is not readable as UTF-8 text. "
            "This does not determine model compatibility."
        ) from exc
    if any(ord(char) < 32 and char not in "\t\r\n" for char in preview):
        raise ValueError(
            "A text preview is unavailable: the file contains binary control characters. "
            "Model compatibility has not been assessed."
        )
    return preview, truncated


def page_heading(eyebrow: str, title: str, description: str) -> None:
    with st.container(gap=None):
        st.markdown(f'<div class="research-eyebrow">{escape(eyebrow)}</div>', unsafe_allow_html=True)
        st.title(title)
        st.markdown(f'<p class="research-description">{escape(description)}</p>', unsafe_allow_html=True)


def status_chip(label: str, tone: str = "pending") -> None:
    st.markdown(chip_html(label, tone), unsafe_allow_html=True)


def chip_html(label: str, tone: str = "default") -> str:
    if tone not in {"default", "pending", "success", "cyan"}:
        raise ValueError("Unsupported status-chip tone")
    return f'<span class="research-chip research-chip--{tone}">{escape(label)}</span>'


def section_card(key: str):
    """A keyed native container keeps its controls accessible and interactive."""
    return st.container(key=f"research-{key}", gap="small")


def system_graphic() -> None:
    st.markdown(
        '<div class="research-system" aria-hidden="true">'
        '<div class="research-system-label">RESEARCH SYSTEM / CONCEPT</div>'
        '<div class="research-orbit"></div><div class="research-orbit research-orbit--inner"></div>'
        + ''.join(f'<div class="research-link research-link--{node}"></div>' for node in "abc")
        + '<div class="research-core"><span>◈</span></div>'
        + ''.join(f'<div class="research-node research-node--{node}"></div>' for node in "abc")
        + '<div class="research-system-caption">Temporal learning · IoT security</div></div>',
        unsafe_allow_html=True,
    )


def workflow_cards() -> None:
    stages = [
        ("01", "Submit", "Choose a file. Keep it available throughout your session.", False),
        ("02", "Inspect", "Review file details and a bounded UTF-8 text preview.", False),
        ("03", "Predict", "Locked. Available after verified model integration.", True),
    ]
    cards = []
    for number, title, description, locked in stages:
        modifier = " research-card--pending" if locked else ""
        lock = '<span class="research-lock" aria-hidden="true"></span> ' if locked else ""
        cards.append(
            f'<article class="research-card{modifier}"><span class="research-step-number">{number}</span>'
            f'<h3>{lock}{title}</h3><p>{description}</p></article>'
        )
    st.markdown('<div class="research-workflow">' + ''.join(cards) + '</div>', unsafe_allow_html=True)


@dataclass(frozen=True)
class Inspection:
    """Presentation outcome of the existing text inspector, never model validation."""

    state: Literal["waiting", "available", "blank", "unavailable"]
    preview: str = ""
    truncated: bool = False
    message: str = ""

    @property
    def label(self) -> str:
        return {
            "waiting": "Awaiting file",
            "available": "Preview available",
            "blank": "No visible text",
            "unavailable": "Preview unavailable",
        }[self.state]


def inspect_file(submitted: SubmittedInput | None) -> Inspection:
    if submitted is None:
        return Inspection("waiting")
    try:
        preview, truncated = text_preview(submitted.content)
    except ValueError as exc:
        return Inspection("unavailable", message=str(exc))
    return Inspection("available" if preview.strip() else "blank", preview, truncated)


def pipeline_status(inspection: Inspection, status: ModelStatus) -> None:
    received = inspection.state != "waiting"
    stages = [
        ("Input", "File received" if received else "Awaiting file", "active" if received else "waiting"),
        ("Inspection", inspection.label, "active" if inspection.state == "available" else "attention" if received else "waiting"),
        ("Preprocessing", "Pending integration", "pending"),
        ("Model", status.message, "pending"),
        ("Prediction", "Locked", "pending"),
    ]
    rows = []
    for index, (name, label, state) in enumerate(stages, 1):
        rows.append(
            f'<li class="is-{state}"><span class="research-pipeline-node" aria-hidden="true">{index:02}</span>'
            f'<div><strong>{escape(name)}</strong><small>{escape(label)}</small></div></li>'
        )
    st.markdown('<ol class="research-pipeline" aria-label="Pipeline status">' + ''.join(rows) + '</ol>', unsafe_allow_html=True)
    st.caption("File inspection only; model compatibility has not been assessed.")
    if inspection.truncated:
        st.caption("Inspection covers the first 8 KiB only.")


def results_empty_state() -> None:
    st.markdown(
        '<div class="research-empty"><div class="research-empty-symbol">'
        '<span class="research-lock" aria-hidden="true"></span></div>'
        '<h3>No prediction available</h3>'
        '<p>Results will appear after verified model integration and a prediction run.</p></div>',
        unsafe_allow_html=True,
    )


def research_flow() -> None:
    stages = ["IoT network traffic", "Temporal / self-supervised GRU-based research", "Planned LOAFO evaluation", "Pending inference integration"]
    st.markdown(
        '<div class="research-flow">' + ''.join(
            f'<div class="research-flow-stage"><span>{index:02} →</span>{escape(stage)}</div>'
            for index, stage in enumerate(stages, 1)
        ) + '</div>', unsafe_allow_html=True,
    )


def submission_controls() -> None:
    st.write("Text preview supports UTF-8 files.")
    st.caption("Model input requirements are not yet available.")
    st.caption("Up to 10 MiB · Kept only for this session; not saved to disk.")
    selected = st.session_state.selected_file
    replacing = st.session_state.replacing_file
    if selected is not None:
        status_chip("File received", "success")
        st.write("File selected. It remains available when you navigate between pages.")
        if not replacing:
            replace_column, clear_column = st.columns(2, gap="small", wrap=True)
            replace_column.button("Replace file", on_click=replace_file, width="stretch")
            clear_column.button("Clear file", on_click=clear_file, width="stretch")
        else:
            st.write("Choose a replacement below. Your current file stays selected until another is received.")
            st.button("Cancel replacement", on_click=cancel_replacement)
    if selected is None or replacing:
        widget_key = f"inspection_upload_{st.session_state.upload_generation}"
        st.file_uploader(
            "Choose a replacement file" if replacing else "Choose a file for inspection",
            key=widget_key,
            on_change=receive_upload,
            args=(widget_key,),
            help="Selecting a file does not validate it for the model.",
        )


def inspect_upload(submitted: SubmittedInput, inspection: Inspection | None = None) -> None:
    inspection = inspection if inspection is not None else inspect_file(submitted)
    st.write("**Selected file**")
    st.text(submitted.filename, width="stretch", wrap=True)
    st.caption(f"File size: {len(submitted.content):,} bytes")
    extension = PurePath(submitted.filename).suffix
    if extension:
        st.caption(f"Filename extension: {extension} · Not a verified file format")
    st.caption("File inspection only; model compatibility has not been assessed.")
    if inspection.state == "unavailable":
        st.warning(inspection.message)
        return
    if inspection.state == "blank":
        st.info("No visible text in this preview.")
    else:
        st.write("**Text preview available**")
        st.code(inspection.preview, language=None, height=280, wrap_lines=True)
    if inspection.truncated:
        st.write("Showing the first 8 KiB only. The remainder has not been inspected.")

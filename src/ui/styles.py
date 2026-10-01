"""Bridge the native theme to a single, application-scoped stylesheet."""

from pathlib import Path
import re

import streamlit as st


def apply_styles() -> None:
    # Only CSS color literals enter this block, never uploaded/user text.
    options = {
        "canvas": "theme.backgroundColor",
        "card": "theme.secondaryBackgroundColor",
        "primary": "theme.textColor",
        "cyan": "theme.primaryColor",
        "elevated": "theme.sidebar.backgroundColor",
    }
    variables = []
    for token, option in options.items():
        color = st.get_option(option)
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError(f"The research theme requires a six-digit hex color for {option}.")
        variables.append(f"--research-{token}: {color};")
    css = Path(__file__).with_name("theme.css").read_text(encoding="utf-8")
    st.html("<style>:root {" + "".join(variables) + "}</style><style>" + css + "</style>")

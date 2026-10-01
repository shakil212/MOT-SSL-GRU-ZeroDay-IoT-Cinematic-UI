"""Session-only uploads, independent of Streamlit's temporary widget state."""

import streamlit as st

from src.inference.contracts import SubmittedInput


def initialize_session() -> None:
    st.session_state.setdefault("selected_file", None)
    st.session_state.setdefault("replacing_file", False)
    st.session_state.setdefault("upload_generation", 0)


def open_submission() -> None:
    st.session_state["workspace_page"] = "Data submission"


def receive_upload(widget_key: str) -> None:
    uploaded = st.session_state.get(widget_key)
    if uploaded is not None:
        st.session_state.selected_file = SubmittedInput(uploaded.name, uploaded.getvalue())
        st.session_state.replacing_file = False


def replace_file() -> None:
    st.session_state.upload_generation += 1
    st.session_state.replacing_file = True


def cancel_replacement() -> None:
    st.session_state.replacing_file = False


def clear_file() -> None:
    st.session_state.selected_file = None
    st.session_state.replacing_file = False
    st.session_state.upload_generation += 1

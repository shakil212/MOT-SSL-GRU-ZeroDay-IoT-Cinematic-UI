"""Launch with: python -m streamlit run app.py."""

import streamlit as st

from src.inference.service import UnavailableInferenceService
from src.ui.components import (
    chip_html, inspect_file, inspect_upload, page_heading, pipeline_status,
    research_flow, results_empty_state, section_card, status_chip,
    submission_controls, system_graphic, workflow_cards,
)
from src.ui.session import initialize_session, open_submission
from src.ui.styles import apply_styles

st.set_page_config(
    page_title="Zero-day IoT | Research demonstrator",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state=260,
)
apply_styles()
initialize_session()
service = UnavailableInferenceService()
status = service.status()

with st.sidebar, st.container(key="research-sidebar"):
    st.markdown(
        '<div class="research-brand"><span class="research-brand-mark" aria-hidden="true">◈</span>'
        '<strong>IoT Research Lab</strong></div>'
        '<div class="research-project-id">MOT-SSL-GRU-ZeroDay-IoT</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="research-sidebar-caption">Research workspace</div>', unsafe_allow_html=True)
    with st.container(key="research-nav"):
        page = st.radio(
            "Navigation", ["Overview", "Data submission", "Research notes"],
            key="workspace_page", label_visibility="collapsed",
        )
    st.space("medium")
    with st.container(key="research-project-status", gap="small"):
        st.caption("PROJECT STAGE")
        st.write("Interface demonstration")
        status_chip(status.message)
        st.caption("File inspection is available. Inference integration is pending.")

with st.container(horizontal_alignment="center"):
    with st.container(width=1240, key="research-shell", gap="medium"):
        st.markdown(
            '<div class="research-toolbar"><span>IoT SECURITY / RESEARCH WORKSPACE</span>'
            '<span>University research demonstrator</span></div>', unsafe_allow_html=True,
        )
        if page == "Overview":
            with st.container(key="research-hero-layout"):
                introduction, graphic = st.columns([1.35, 1], gap="large", vertical_alignment="center", wrap=True)
                with introduction:
                    page_heading(
                        "Machine Learning / Cybersecurity Research",
                        "Zero-day IoT Intrusion Detection",
                        "Exploring temporal and self-supervised GRU-based learning for zero-day intrusion detection in IoT networks.",
                    )
                    st.caption("STATED RESEARCH DIRECTION")
                    st.markdown(
                        '<div class="research-chips">'
                        + chip_html("Temporal GRU", "cyan")
                        + chip_html("Self-supervised learning")
                        + chip_html("LOAFO evaluation · planned")
                        + chip_html("Model integration pending", "pending") + '</div>',
                        unsafe_allow_html=True,
                    )
                    st.button("Open data submission", type="primary", on_click=open_submission)
                with graphic:
                    system_graphic()
            with st.container(gap="small"):
                st.header("Explore the demonstration", anchor=False)
                st.caption("From file submission to inspection. Prediction awaits model integration.")
                workflow_cards()
            st.markdown(
                '<p class="research-inline-note">Evaluation plan: strict Leave-One-Attack-Family-Out (LOAFO). '
                'Explore the approach and current stage in Research notes.</p>', unsafe_allow_html=True,
            )

        elif page == "Data submission":
            page_heading(
                "Interactive demonstration",
                "Submit and inspect data",
                "Review a file, inspect its contents, and explore the planned prediction workflow.",
            )
            submitted = st.session_state.selected_file
            inspection = inspect_file(submitted)
            with st.container(key="research-submission-layout"):
                left, right = st.columns([3, 2], gap="medium", wrap=True)
                with left:
                    with section_card("upload"):
                        st.header("01 / Submit file", anchor=False)
                        submission_controls()
                    with section_card("inspection"):
                        st.header("02 / Inspect file", anchor=False)
                        if submitted is None:
                            st.info("No file selected. Choose a file above to see its details and text preview here.")
                        else:
                            inspect_upload(submitted, inspection)
                with right:
                    with section_card("pipeline"):
                        st.header("ML pipeline", anchor=False)
                        pipeline_status(inspection, status)
                    with section_card("results"):
                        st.header("03 / Prediction", anchor=False)
                        st.info(f"No prediction available — {status.message}.")
                        st.button("Run prediction", disabled=True, type="primary", width="stretch")
                        st.subheader("Results", anchor=False)
                        results_empty_state()
                        with st.expander("About future results"):
                            st.write("The model is being trained separately in Google Colab. Prediction will become available after verified integration.")
                            st.write("Confidence or probability will be shown only if supported by the trained model.")

        else:
            page_heading(
                "Research context",
                "The research behind the interface",
                "The stated learning approach, planned evaluation, and path to verified model integration.",
            )
            with st.container(gap="small"):
                st.header("Proposed research workflow", anchor=False)
                st.caption("Research direction only; this is not a verified executable pipeline.")
                research_flow()
            with st.container(key="research-notes-layout", gap="medium"):
                objective, evaluation = st.columns(2, gap="medium", wrap=True)
                with objective, section_card("methodology"):
                    st.header("Methodology", anchor=False)
                    status_chip("Stated approach", "cyan")
                    st.write("Investigate zero-day IoT intrusion detection using temporal and self-supervised GRU-based learning.")
                    with st.expander("About the learning approach"):
                        st.write("These are the project's stated research directions. Their implementation and sequencing remain pending review of the actual training notebook.")
                with evaluation, section_card("evaluation"):
                    st.header("LOAFO evaluation", anchor=False)
                    status_chip("Evaluation planned")
                    st.write("Strict Leave-One-Attack-Family-Out (LOAFO) evaluation is the planned research protocol.")
                    with st.expander("Evaluation status"):
                        st.write("Verified research results are not yet available in this demonstration. No accuracy, attack distributions, or evaluation metrics are reported.")
                training, provenance = st.columns(2, gap="medium", wrap=True)
                with training, section_card("training"):
                    st.header("Training & integration", anchor=False)
                    status_chip("Integration pending")
                    st.write("Training is maintained separately in Google Colab. The application currently demonstrates file submission and inspection.")
                    st.caption("Trained exports have not been supplied. Model-specific input requirements and preprocessing remain unverified.")
                with provenance, section_card("provenance"):
                    st.header("Research provenance", anchor=False)
                    st.caption("DOCUMENTED TRAINING NOTEBOOK")
                    st.text("ZeroDay_IoT_Final_Training.ipynb", wrap=True)
                    status_chip("Reference notebook not supplied")
                    with st.expander("Artifact and experiment status"):
                        st.write("The reference notebook, trained exports, and verified results have not been supplied. Experiment provenance cannot be verified yet.")
                        st.write("Notebook revision, model bundle identity, and evaluation-fold provenance will be recorded when verified artifacts are available.")

        st.markdown(
            '<footer class="research-footer"><span>MOT-SSL-GRU-ZeroDay-IoT</span>'
            '<span>University research demonstration · Model not connected</span></footer>',
            unsafe_allow_html=True,
        )

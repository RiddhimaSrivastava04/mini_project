"""Streamlit entry point for the question answering application."""

from __future__ import annotations

import logging

import streamlit as st

from app.config.settings import ConfigurationError, load_settings
from app.prompts.qa_prompt import SYSTEM_PROMPT
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def _initialize_conversation() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def _display_messages() -> None:
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    """Render the Streamlit application."""
    configure_logging()
    st.set_page_config(page_title="AI Question & Answering System", page_icon="💬")
    st.title("AI Question & Answering System")
    st.write("Ask questions and receive answers powered by Google Gemini.")

    try:
        settings = load_settings()
    except ConfigurationError as exc:
        st.error(str(exc))
        st.stop()

    service = GeminiService(settings)
    _initialize_conversation()

    with st.sidebar:
        st.subheader("Settings")
        st.caption(f"Model: `{settings.gemini_model}`")
        st.caption(f"Temperature: `{settings.temperature:g}`")
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

    _display_messages()
    question = st.chat_input("Ask a question...")
    if question is None:
        return

    question = question.strip()
    if not question:
        st.warning("Please enter a question before submitting.")
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating an answer..."):
            try:
                answer = service.generate_answer(st.session_state.messages)
            except GeminiServiceError as exc:
                logger.warning("Answer request could not be completed.")
                st.error(str(exc))
                return
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()

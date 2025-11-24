"""Main Streamlit application - Home page."""

import streamlit as st


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="GC Streamlit",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🚀 GC Streamlit")
    st.write("This is a multi-page Streamlit application running in Docker.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Info")
        st.info("Built with Python 3.13 and Streamlit")
        st.code("docker run -p 8501:8501 gc-streamlit")

    with col2:
        st.subheader("Getting Started")
        st.success("Edit app/main.py to customize this page")
        st.write("Changes will hot-reload automatically in dev mode!")

    st.divider()

    # Navigation hint
    st.subheader("📑 Multiple Pages")
    st.write("Check out the **About** page in the sidebar to learn more about this application!")

    # Simple interaction
    name = st.text_input("What's your name?", placeholder="Enter your name")
    if name:
        st.balloons()
        st.write(f"Hello, {name}! 👋")


if __name__ == "__main__":
    main()

"""About page for GC Streamlit application."""

import streamlit as st
import base64
from pathlib import Path


def load_google_sans_font():
    """Load Google Sans Flex font from local file and embed it."""
    font_path = Path(__file__).parent.parent / "static" / "fonts" / "GoogleSansFlex-Latin.woff2"

    # Read and encode font file to base64
    with open(font_path, "rb") as f:
        font_data = base64.b64encode(f.read()).decode()

    # Inject font CSS with base64 data and apply to all elements
    st.markdown(f"""
        <style>
        @font-face {{
            font-family: 'Google Sans Flex';
            font-style: normal;
            font-weight: 400 700;
            font-stretch: 100%;
            font-display: block;
            src: url(data:font/woff2;base64,{font_data}) format('woff2');
        }}

        html, body, [class*="css"], * {{
            font-family: 'Google Sans Flex', sans-serif !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Google Sans Flex', sans-serif !important;
        }}

        .stMarkdown, .stText, .stTextInput, .stSelectbox, .stMultiselect,
        .stNumberInput, .stTextArea, .stDateInput, .stTimeInput,
        div[data-testid="stMarkdownContainer"], p, span, label {{
            font-family: 'Google Sans Flex', sans-serif !important;
        }}

        /* Hide the keyboard_double_arrow_left text completely */
        span {{
            position: relative;
        }}

        /* Target spans that contain the text and hide it */
        [data-testid="stSidebarCollapse"] span,
        [data-testid="collapsedControl"] span,
        button[kind="header"] span,
        button[kind="headerNoPadding"] span {{
            font-size: 0 !important;
        }}

        /* Add Unicode replacement symbol */
        [data-testid="stSidebarCollapse"] span::before,
        [data-testid="collapsedControl"] span::before,
        button[kind="header"] span::before,
        button[kind="headerNoPadding"] span::before {{
            content: "«";
            font-size: 1.5rem !important;
            font-family: 'Google Sans Flex', sans-serif !important;
        }}
        </style>
        """, unsafe_allow_html=True)


def main():
    """About page content."""
    st.set_page_config(
        page_title="About - GC Streamlit",
        page_icon="ℹ️",
        layout="wide",
    )

    # Apply Google Sans font for Material Design look (local, no FOUC)
    load_google_sans_font()

    st.title("ℹ️ About GC Streamlit")

    st.markdown("""
    ## Overview

    This is a production-ready Docker scaffold for Python Streamlit applications,
    demonstrating multi-page routing and modern development practices.

    ## Features

    - 🐍 **Python 3.13** - Latest stable Python version
    - ⚡ **uv** - Blazing fast Python package installer
    - 🚀 **Streamlit** - Modern web app framework
    - 🐳 **Multi-stage Docker** - Optimized builds for dev and prod
    - 🔥 **Hot-reload** - Automatic reload on code changes in dev mode
    - 🔒 **SSL/HTTPS support** - Production-ready with nginx reverse proxy
    - ✅ **Testing** - pytest with coverage reporting
    - 🎨 **Code quality** - ruff for fast linting and formatting
    - 📄 **Multi-page routing** - Demonstrated with this About page!

    ## Technology Stack

    | Component | Version | Purpose |
    |-----------|---------|---------|
    | Python | 3.13 | Programming language |
    | Streamlit | Latest | Web framework |
    | uv | Latest | Package management |
    | Docker | Latest | Containerization |
    | pytest | Latest | Testing framework |
    | ruff | Latest | Linting and formatting |

    ## Multi-Page Routing

    Streamlit automatically creates navigation from files in the `pages/` directory.
    Each Python file becomes a page in the sidebar navigation. The file name
    determines the page name in the sidebar.

    ### How it works:
    - `app/main.py` → Home page (always first)
    - `app/pages/about.py` → About page (you are here!)
    - `app/pages/xyz.py` → Would create an "Xyz" page

    """)

    st.divider()

    # Project metadata
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Python Version", "3.13")

    with col2:
        st.metric("Docker", "Multi-stage")

    with col3:
        st.metric("Hot Reload", "Enabled")

    st.divider()

    # Additional info
    with st.expander("📚 Learn More"):
        st.markdown("""
        ### Resources
        - [Streamlit Documentation](https://docs.streamlit.io/)
        - [Python 3.13 Docs](https://docs.python.org/3.13/)
        - [uv Package Manager](https://github.com/astral-sh/uv)
        - [Docker Documentation](https://docs.docker.com/)

        ### Author
        Glenn Cueto

        ### License
        MIT
        """)


if __name__ == "__main__":
    main()

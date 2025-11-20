"""Tests for the main Streamlit application (home page)."""

import pytest
from unittest.mock import patch, MagicMock


def test_main_page_title():
    """Test that the main page sets the correct title."""
    with patch("streamlit.set_page_config") as mock_config, \
         patch("streamlit.title") as mock_title, \
         patch("streamlit.write"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.text_input"):

        # Mock columns to return context managers
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main
        from app.main import main
        main()

        # Verify page config was set
        mock_config.assert_called_once_with(
            page_title="GC Streamlit",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # Verify title was set
        mock_title.assert_called_once_with("🚀 Welcome to GC Streamlit")


def test_main_page_renders_without_errors():
    """Test that the main page renders without raising exceptions."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.write"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.info"), \
         patch("streamlit.code"), \
         patch("streamlit.success"), \
         patch("streamlit.text_input", return_value=""):

        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main - should not raise
        from app.main import main
        main()


def test_main_page_name_input():
    """Test that entering a name triggers the greeting."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.write") as mock_write, \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.subheader"), \
         patch("streamlit.info"), \
         patch("streamlit.code"), \
         patch("streamlit.success"), \
         patch("streamlit.text_input", return_value="Alice"), \
         patch("streamlit.balloons"):

        # Mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Import and run main
        from app.main import main
        main()

        # Check that greeting was written
        calls = [str(call) for call in mock_write.call_args_list]
        assert any("Alice" in call for call in calls), "Expected greeting with name 'Alice'"

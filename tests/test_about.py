"""Tests for the About page."""

import pytest
from unittest.mock import patch, MagicMock


def test_about_page_title():
    """Test that the about page sets the correct title."""
    with patch("streamlit.set_page_config") as mock_config, \
         patch("streamlit.title") as mock_title, \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric"), \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main
        from app.pages.about import main
        main()

        # Verify page config was set
        mock_config.assert_called_once_with(
            page_title="About - GC Streamlit",
            page_icon="ℹ️",
            layout="wide",
        )

        # Verify title was set
        mock_title.assert_called_once_with("ℹ️ About GC Streamlit")


def test_about_page_renders_without_errors():
    """Test that the about page renders without raising exceptions."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric"), \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main - should not raise
        from app.pages.about import main
        main()


def test_about_page_displays_metrics():
    """Test that the about page displays project metrics."""
    with patch("streamlit.set_page_config"), \
         patch("streamlit.title"), \
         patch("streamlit.markdown"), \
         patch("streamlit.divider"), \
         patch("streamlit.columns") as mock_columns, \
         patch("streamlit.metric") as mock_metric, \
         patch("streamlit.expander") as mock_expander:

        # Mock columns and expander
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()

        # Import and run main
        from app.pages.about import main
        main()

        # Verify metrics were created
        assert mock_metric.call_count == 3
        calls = [call[0] for call in mock_metric.call_args_list]
        labels = [call[0] for call in calls]
        assert "Python Version" in labels
        assert "Docker" in labels
        assert "Hot Reload" in labels

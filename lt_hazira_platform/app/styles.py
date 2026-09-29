"""Custom CSS styles for Streamlit application with L&T industrial theme."""

CUSTOM_CSS = """
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #004b87;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #004b87;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
    }
    .risk-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .risk-normal {
        color: #28a745;
        font-weight: bold;
    }
</style>
"""

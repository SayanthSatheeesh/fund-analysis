import streamlit as st

def apply_custom_theme():
    """Inject custom CSS for premium styling."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background-color: #0E1117;
        }
        
        /* Metric Card Styling */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid #00D4FF;
        }
        
        /* Glassmorphism Sidebar */
        .sidebar .sidebar-content {
            background: rgba(14, 17, 23, 0.95);
            backdrop-filter: blur(10px);
        }
        
        /* Custom Header */
        h1 {
            background: linear-gradient(90deg, #00D4FF, #0072FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

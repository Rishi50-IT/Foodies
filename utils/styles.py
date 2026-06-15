"""Shared CSS — Zomato/Swiggy-inspired look."""
import streamlit as st

PRIMARY = "#FC8019"   # Swiggy orange
ACCENT = "#E23744"    # Zomato red

CSS = f"""
<style>
:root {{
  --primary: {PRIMARY};
  --accent: {ACCENT};
}}
.block-container {{ padding-top: 1.2rem; max-width: 1200px; }}
h1, h2, h3 {{ font-family: 'Segoe UI', system-ui, sans-serif; }}

.fr-hero {{
  background: linear-gradient(135deg, {PRIMARY} 0%, {ACCENT} 100%);
  color: white; padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem;
}}
.fr-hero h1 {{ color: white; margin: 0 0 .5rem 0; }}

.fr-card {{
  background: white; border-radius: 14px; padding: 1rem;
  box-shadow: 0 2px 10px rgba(0,0,0,.06);
  transition: transform .15s ease, box-shadow .15s ease;
  margin-bottom: 1rem;
}}
.fr-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,.1); }}
.fr-img {{ width: 100%; height: 160px; object-fit: cover; border-radius: 10px; }}
.fr-title {{ font-weight: 700; font-size: 1.05rem; margin: .5rem 0 .2rem; }}
.fr-meta  {{ color: #666; font-size: .85rem; }}
.fr-price {{ font-weight: 700; color: var(--accent); font-size: 1.1rem; }}
.fr-mrp   {{ text-decoration: line-through; color: #999; margin-left: .4rem; font-size: .85rem; }}
.fr-disc  {{ color: #2e7d32; font-weight: 600; margin-left: .4rem; font-size: .85rem; }}

.badge {{ display:inline-block; padding: 2px 8px; border-radius: 6px; font-size: .72rem;
  font-weight: 700; margin-right: 4px; }}
.b-veg     {{ background:#e8f5e9; color:#2e7d32; border:1px solid #2e7d32; }}
.b-nonveg  {{ background:#ffebee; color:#c62828; border:1px solid #c62828; }}
.b-best    {{ background:#fff3e0; color:#e65100; }}
.b-free    {{ background:#e3f2fd; color:#1565c0; }}
.b-off     {{ background:{ACCENT}; color:white; }}

.fr-cat {{
  background:white; border-radius:50%; width:80px; height:80px;
  display:flex; align-items:center; justify-content:center; font-size:2rem;
  box-shadow:0 2px 8px rgba(0,0,0,.08); margin: 0 auto;
}}
.stButton>button {{
  background: var(--primary); color: white; border: none;
  border-radius: 8px; padding: .45rem 1rem; font-weight: 600;
}}
.stButton>button:hover {{ background: var(--accent); color:white; }}
</style>
"""


def inject():
    st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background: #2d2d2d !important;
    opacity: 1 !important;
}

/* Remove blur and transparency */
[data-testid="stSidebar"] > div:first-child {
    background-color: #2d2d2d !important;
    backdrop-filter: none !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Input boxes */
.stTextInput input {
    background-color: white !important;
    color: black !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
    st.markdown(CSS, unsafe_allow_html=True)

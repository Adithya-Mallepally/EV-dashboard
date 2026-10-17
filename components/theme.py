"""
components/theme.py
───────────────────
DeLorean Marketplace visual design system.
Replicates the aesthetic of https://marketplace.delorean.com/
- Fonts: TT Mussels (Display), Neue Haas Grotesk (UI/Body), Maison Neue Mono (Data/Telemetry)
- Color Palette: Obsidian Dark (#0e0e11), Carbon Surface (#16161a), DeLorean Redshift (#de1e14),
  Brushed Steel (#e2e8f0), Slate Borders (#27272f)
- Zero emojis and zero icons across all UI elements.
"""

import os
import base64
import streamlit as st

_FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")

@st.cache_data
def _load_font_b64(filename: str) -> str:
    path = os.path.join(_FONTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as fh:
            return base64.b64encode(fh.read()).decode("utf-8")
    return ""


def get_delorean_css() -> str:
    """Generate the full CSS stylesheet replicating DeLorean Marketplace."""
    nhg_b64 = _load_font_b64("NeueHaasGrotesk.ttf")
    nhg_bold_b64 = _load_font_b64("NeueHaasGroteskBold.ttf")
    ttm_b64 = _load_font_b64("TTMussels.otf")
    mnm_b64 = _load_font_b64("MaisonNeueMono.otf")

    font_faces = []
    if nhg_b64:
        font_faces.append(f"""
        @font-face {{
            font-family: 'NeueHaasGrotesk';
            src: url('data:font/truetype;charset=utf-8;base64,{nhg_b64}') format('truetype');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}""")
    if nhg_bold_b64:
        font_faces.append(f"""
        @font-face {{
            font-family: 'NeueHaasGrotesk';
            src: url('data:font/truetype;charset=utf-8;base64,{nhg_bold_b64}') format('truetype');
            font-weight: 700;
            font-style: normal;
            font-display: swap;
        }}""")
    if ttm_b64:
        font_faces.append(f"""
        @font-face {{
            font-family: 'TTMussels';
            src: url('data:font/opentype;charset=utf-8;base64,{ttm_b64}') format('opentype');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}""")
    if mnm_b64:
        font_faces.append(f"""
        @font-face {{
            font-family: 'MaisonNeueMono';
            src: url('data:font/opentype;charset=utf-8;base64,{mnm_b64}') format('opentype');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}""")

    font_css = "\n".join(font_faces)

    return f"""
    <style>
    {font_css}

    /* ── Global Theme & Reset ─────────────────────────────────────────── */
    html, body, [class*="css"], .stApp {{
        background-color: #0e0e11 !important;
        color: #f4f4f5 !important;
        font-family: 'NeueHaasGrotesk', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .main .block-container {{
        max-width: 1440px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }}

    /* ── Typography ──────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'TTMussels', 'NeueHaasGrotesk', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }}

    p, span, label, div {{
        font-family: 'NeueHaasGrotesk', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}

    code, pre, .mono-data {{
        font-family: 'MaisonNeueMono', monospace !important;
    }}

    hr {{
        border: none !important;
        border-top: 1px solid #232328 !important;
        margin: 2rem 0 !important;
    }}

    /* ── Sidebar (DeLorean Obsidian) ─────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background-color: #0a0a0d !important;
        border-right: 1px solid #232328 !important;
        padding-top: 1.5rem !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: #f4f4f5 !important;
        font-family: 'NeueHaasGrotesk', sans-serif;
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        font-family: 'TTMussels', sans-serif !important;
        letter-spacing: 0.08em !important;
        font-size: 13px !important;
        color: #a1a1aa !important;
        text-transform: uppercase !important;
        margin-bottom: 0.75rem !important;
    }}

    /* ── Native Streamlit Metrics ────────────────────────────────────── */
    div[data-testid="stMetric"] {{
        background-color: #16161a !important;
        border: 1px solid #27272f !important;
        border-top: 2px solid #de1e14 !important;
        border-radius: 2px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }}

    div[data-testid="stMetric"]:hover {{
        border-color: #3d3f47 !important;
        border-top: 2px solid #de1e14 !important;
    }}

    div[data-testid="stMetric"] label {{
        font-family: 'MaisonNeueMono', monospace !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 0.12em !important;
        color: #8e8e98 !important;
        font-weight: 500 !important;
    }}

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        font-family: 'NeueHaasGrotesk', sans-serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
    }}

    /* ── Form Controls & Inputs (DeLorean Industrial) ─────────────────── */
    input, select, textarea, div[data-baseweb="select"] > div {{
        background-color: #16161a !important;
        border: 1px solid #282830 !important;
        border-radius: 2px !important;
        color: #ffffff !important;
        font-family: 'NeueHaasGrotesk', sans-serif !important;
        font-size: 14px !important;
    }}

    div[data-baseweb="select"] > div:hover,
    input:focus, select:focus {{
        border-color: #de1e14 !important;
        outline: none !important;
        box-shadow: 0 0 0 1px #de1e14 !important;
    }}

    div[data-baseweb="tag"] {{
        background-color: #27282d !important;
        border: 1px solid #3d3f47 !important;
        border-radius: 2px !important;
        font-family: 'MaisonNeueMono', monospace !important;
        font-size: 11px !important;
        color: #ffffff !important;
    }}

    /* ── Buttons (DeLorean Redshift Accent) ────────────────────────────── */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {{
        background-color: #de1e14 !important;
        color: #ffffff !important;
        font-family: 'TTMussels', 'NeueHaasGrotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        border: 1px solid #de1e14 !important;
        border-radius: 2px !important;
        padding: 0.6rem 1.4rem !important;
        transition: background-color 0.2s ease, border-color 0.2s ease !important;
    }}

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {{
        background-color: #b8150d !important;
        border-color: #b8150d !important;
    }}

    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {{
        background-color: #16161a !important;
        color: #e4e4e7 !important;
        font-family: 'MaisonNeueMono', monospace !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        border: 1px solid #2d2d36 !important;
        border-radius: 2px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.2s ease, border-color 0.2s ease !important;
    }}

    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        background-color: #22222a !important;
        border-color: #3d3f47 !important;
        color: #ffffff !important;
    }}

    /* ── Sliders (DeLorean Precision Track) ────────────────────────────── */
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: #de1e14 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 8px rgba(222, 30, 20, 0.6) !important;
    }}

    div[data-testid="stSlider"] div[data-baseweb="slider"] div {{
        font-family: 'MaisonNeueMono', monospace !important;
    }}

    /* ── Data Tables ─────────────────────────────────────────────────── */
    div[data-testid="stDataFrame"] {{
        background-color: #141417 !important;
        border: 1px solid #232328 !important;
        border-radius: 2px !important;
    }}

    /* ── Notifications / Alerts ──────────────────────────────────────── */
    div[data-testid="stAlert"] {{
        background-color: #16161a !important;
        border: 1px solid #282830 !important;
        border-left: 3px solid #de1e14 !important;
        border-radius: 2px !important;
        color: #f4f4f5 !important;
        font-family: 'NeueHaasGrotesk', sans-serif !important;
    }}

    div[data-testid="stAlert"] * {{
        color: #f4f4f5 !important;
    }}

    /* Hide any default icon svgs in stAlert if present */
    div[data-testid="stAlert"] svg {{
        display: none !important;
    }}

    /* ── Custom DeLorean Component Classes ────────────────────────────── */
    .delorean-header {{
        border-bottom: 1px solid #232328;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }}

    .delorean-eyebrow {{
        font-family: 'MaisonNeueMono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #de1e14;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .delorean-title {{
        font-family: 'TTMussels', sans-serif;
        font-size: 34px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        line-height: 1.1;
    }}

    .delorean-subtitle {{
        font-family: 'NeueHaasGrotesk', sans-serif;
        font-size: 15px;
        color: #a1a1aa;
        line-height: 1.5;
        max-width: 900px;
    }}

    .delorean-card {{
        background: #16161a;
        border: 1px solid #27272f;
        border-top: 2px solid #de1e14;
        padding: 20px 22px;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        height: 100%;
        transition: border-color 0.2s ease;
    }}

    .delorean-card:hover {{
        border-color: #3d3f47;
        border-top: 2px solid #de1e14;
    }}

    .delorean-card-label {{
        font-family: 'MaisonNeueMono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #8e8e98;
        margin-bottom: 6px;
    }}

    .delorean-card-value {{
        font-family: 'NeueHaasGrotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    .delorean-card-meta {{
        font-family: 'MaisonNeueMono', monospace;
        font-size: 11px;
        color: #71717a;
        margin-top: 6px;
    }}

    .delorean-section-header {{
        font-family: 'TTMussels', sans-serif;
        font-size: 18px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #ffffff;
        margin: 1.5rem 0 0.25rem 0;
    }}

    .delorean-section-sub {{
        font-family: 'NeueHaasGrotesk', sans-serif;
        font-size: 13px;
        color: #8e8e98;
        margin-bottom: 1.25rem;
    }}

    .delorean-footer {{
        border-top: 1px solid #232328;
        padding-top: 2rem;
        margin-top: 3rem;
        text-align: center;
        font-family: 'MaisonNeueMono', monospace;
        font-size: 11px;
        color: #71717a;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    /* ── Hide Streamlit default hamburger menu & footer ────────────── */
    #MainMenu, footer {{
        visibility: hidden;
    }}
    </style>
    """


def inject_delorean_theme():
    """Injects DeLorean design system stylesheet into the Streamlit app."""
    st.markdown(get_delorean_css(), unsafe_allow_html=True)

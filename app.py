import streamlit as st
from googletrans import Translator, LANGUAGES
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="LinguaAI — Neural Translation",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #070810 !important;
    color: #e8e6f0 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #1a0a3d 0%, #070810 60%) !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.block-container {
    max-width: 1100px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}

/* Hero */
.hero {
    text-align: center;
    padding: 4rem 0 3rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(120,80,255,0.08) 0%, transparent 70%);
    top: -100px; left: 50%; transform: translateX(-50%);
    pointer-events: none; border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(120,80,255,0.15);
    border: 1px solid rgba(120,80,255,0.4);
    color: #a78bfa;
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(232,230,240,0.5);
    font-weight: 300;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Stats Bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 3rem;
    padding: 1.5rem 0 3rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 3rem;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #a78bfa;
}
.stat-label {
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(232,230,240,0.35);
    font-family: 'Fira Code', monospace;
    margin-top: 0.2rem;
}

/* Section labels */
.section-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(232,230,240,0.35);
    margin-bottom: 0.6rem;
}

/* Selectbox */
[data-testid="stSelectbox"] * { color: #e8e6f0 !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 14px !important;
}
[data-testid="stSelectbox"] svg { fill: #a78bfa !important; }
div[data-baseweb="select"] { background: transparent !important; }
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 14px !important;
    color: #e8e6f0 !important;
}
div[data-baseweb="select"] > div > div { color: #e8e6f0 !important; }
div[data-baseweb="select"] span { color: #e8e6f0 !important; }
div[data-baseweb="menu"] { background: #0f0f1a !important; }
div[data-baseweb="menu"] li { color: #e8e6f0 !important; background: #0f0f1a !important; }
div[data-baseweb="menu"] li:hover { background: rgba(167,139,250,0.15) !important; }

/* Text Areas */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    color: #e8e6f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    padding: 1.2rem 1.4rem !important;
    resize: none !important;
    transition: border-color 0.25s, box-shadow 0.25s;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 0 3px rgba(120,80,255,0.12), 0 0 30px rgba(120,80,255,0.08) !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: rgba(232,230,240,0.2) !important; }
[data-testid="stTextArea"] label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: rgba(232,230,240,0.35) !important;
}

/* Button */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.35) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.5) !important;
    background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* Output Card */
.output-card {
    background: rgba(167,139,250,0.05);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 40px rgba(120,80,255,0.06);
    min-height: 220px;
}
.output-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.output-label::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    background: #a78bfa;
    border-radius: 50%;
    box-shadow: 0 0 8px #a78bfa;
}
.output-text {
    font-size: 1.15rem;
    font-weight: 300;
    line-height: 1.75;
    color: #e8e6f0;
    font-family: 'Inter', sans-serif;
}
.output-meta {
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.output-meta-item {
    font-family: 'Fira Code', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: rgba(232,230,240,0.25);
    text-transform: uppercase;
}
.output-meta-item span {
    color: rgba(167,139,250,0.7);
    margin-left: 0.3rem;
}
.output-empty {
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(232,230,240,0.12);
    font-family: 'Fira Code', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
}

/* Char counter */
.char-counter {
    text-align: right;
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    color: rgba(232,230,240,0.2);
    margin-top: 0.3rem;
    margin-bottom: 1rem;
}
.char-warn { color: rgba(251,191,36,0.55) !important; }
.char-danger { color: rgba(248,113,113,0.65) !important; }

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    background: rgba(120,80,255,0.08) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Features */
.features-section {
    margin-top: 5rem;
    padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.features-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 2rem;
    color: rgba(232,230,240,0.85);
}
.feat-grid { display: flex; gap: 1rem; flex-wrap: wrap; }
.feat-card {
    flex: 1 1 180px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    transition: border-color 0.2s, transform 0.2s;
}
.feat-card:hover { border-color: rgba(167,139,250,0.3); transform: translateY(-3px); }
.feat-icon { font-size: 1.6rem; margin-bottom: 0.8rem; }
.feat-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
    color: #e8e6f0;
}
.feat-desc { font-size: 0.82rem; color: rgba(232,230,240,0.4); line-height: 1.5; font-weight: 300; }

/* Footer */
.site-footer {
    text-align: center;
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-size: 0.78rem;
    color: rgba(232,230,240,0.15);
    font-family: 'Fira Code', monospace;
    letter-spacing: 0.05em;
}

/* Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero { animation: fadeUp 0.6s ease both; }
.stats-bar { animation: fadeUp 0.6s ease 0.1s both; }
.feat-card { animation: fadeUp 0.6s ease both; }
.feat-card:nth-child(2) { animation-delay: 0.08s; }
.feat-card:nth-child(3) { animation-delay: 0.16s; }
.feat-card:nth-child(4) { animation-delay: 0.24s; }
.feat-card:nth-child(5) { animation-delay: 0.32s; }

[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LANGUAGE MAP
# ---------------------------------------------------
LANG_DISPLAY = {name.title(): code for code, name in LANGUAGES.items()}
LANG_DISPLAY_SORTED = dict(sorted(LANG_DISPLAY.items()))
LANG_NAMES = list(LANG_DISPLAY_SORTED.keys())

# ---------------------------------------------------
# HERO
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Google Translate · 100+ Languages</div>
    <h1>Break Every<br>Language Barrier</h1>
    <p class="hero-sub">
        Lightning-fast translation across 100+ languages —
        names respected, auto-detection built-in, deploy anywhere for free.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-bar">
    <div class="stat-item"><div class="stat-num">100+</div><div class="stat-label">Languages</div></div>
    <div class="stat-item"><div class="stat-num">Google</div><div class="stat-label">Translation Engine</div></div>
    <div class="stat-item"><div class="stat-num">Auto</div><div class="stat-label">Language Detection</div></div>
    <div class="stat-item"><div class="stat-num">Free</div><div class="stat-label">No API Key Needed</div></div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LANGUAGE SELECTORS
# ---------------------------------------------------
sel_col1, sel_col2, sel_col3 = st.columns([5, 1, 5])

with sel_col1:
    st.markdown('<p class="section-label">Source Language</p>', unsafe_allow_html=True)
    src_options = ["🔍 Auto Detect"] + LANG_NAMES
    source_lang = st.selectbox(
        "Source Language", src_options, index=0,
        label_visibility="collapsed", key="src_lang"
    )

with sel_col2:
    st.markdown(
        '<div style="display:flex;align-items:center;justify-content:center;'
        'padding-top:1.8rem;color:rgba(167,139,250,0.45);font-size:1.3rem;">⇄</div>',
        unsafe_allow_html=True
    )

with sel_col3:
    st.markdown('<p class="section-label">Target Language</p>', unsafe_allow_html=True)
    hindi_idx = LANG_NAMES.index("Hindi") if "Hindi" in LANG_NAMES else 0
    target_lang = st.selectbox(
        "Target Language", LANG_NAMES, index=hindi_idx,
        label_visibility="collapsed", key="tgt_lang"
    )

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TRANSLATOR
# ---------------------------------------------------
@st.cache_resource
def get_translator():
    return Translator()

translator = get_translator()

# ---------------------------------------------------
# TRANSLATE FUNCTION
# ---------------------------------------------------
def translate_text(text, src_code, dest_code):
    result = translator.translate(text, src=src_code, dest=dest_code)
    return result.text, result.src

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
for key, default in [
    ("translation_result", ""),
    ("detected_lang", ""),
    ("elapsed", 0.0),
    ("char_count", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------
# INPUT / OUTPUT
# ---------------------------------------------------
col1, col_mid, col2 = st.columns([10, 1, 10])

with col1:
    input_text = st.text_area(
        "Source Text",
        placeholder="Type or paste your text here…",
        height=220,
        key="input_text",
        label_visibility="visible"
    )
    char_count = len(input_text)
    if char_count > 4500:
        counter_cls = "char-counter char-danger"
    elif char_count > 3500:
        counter_cls = "char-counter char-warn"
    else:
        counter_cls = "char-counter"
    st.markdown(
        f'<p class="{counter_cls}">{char_count} / 5000 characters</p>',
        unsafe_allow_html=True
    )

with col_mid:
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

with col2:
    st.markdown('<p class="section-label">Translation Output</p>', unsafe_allow_html=True)

    if st.session_state.translation_result:
        detected_name = LANGUAGES.get(
            st.session_state.detected_lang,
            st.session_state.detected_lang
        ).title()
        st.markdown(f"""
        <div class="output-card">
            <div class="output-label">Translation ready</div>
            <div class="output-text">{st.session_state.translation_result}</div>
            <div class="output-meta">
                <div class="output-meta-item">Detected<span>{detected_name}</span></div>
                <div class="output-meta-item">Time<span>{st.session_state.elapsed}s</span></div>
                <div class="output-meta-item">Characters<span>{st.session_state.char_count}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="output-card output-empty">AWAITING INPUT</div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# TRANSLATE BUTTON
# ---------------------------------------------------
st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

b1, b2, b3 = st.columns([3, 4, 3])
with b2:
    if st.button("✦  Translate Now", use_container_width=True):
        if not input_text.strip():
            st.warning("Please enter some text before translating.")
        elif len(input_text) > 5000:
            st.warning("Text exceeds 5000 characters. Please shorten your input.")
        elif source_lang != "🔍 Auto Detect" and source_lang == target_lang:
            st.warning("Source and target language are the same.")
        else:
            src_code = "auto" if source_lang == "🔍 Auto Detect" else LANG_DISPLAY_SORTED[source_lang]
            dest_code = LANG_DISPLAY_SORTED[target_lang]

            with st.spinner("Translating…"):
                try:
                    start = time.time()
                    result_text, detected = translate_text(input_text, src_code, dest_code)
                    elapsed = round(time.time() - start, 2)

                    st.session_state.translation_result = result_text
                    st.session_state.detected_lang = detected
                    st.session_state.elapsed = elapsed
                    st.session_state.char_count = len(input_text)
                    st.rerun()

                except Exception as e:
                    st.error(f"Translation failed: {e}. Check your internet connection.")

# ---------------------------------------------------
# FEATURES
# ---------------------------------------------------
st.markdown("""
<div class="features-section">
    <p class="features-title">Why LinguaAI?</p>
    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon">🌍</div>
            <div class="feat-name">100+ Languages</div>
            <div class="feat-desc">From Afrikaans to Zulu — Google's engine covers virtually every major language on Earth.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🔍</div>
            <div class="feat-name">Auto Detection</div>
            <div class="feat-desc">Don't know the source language? Just paste the text and LinguaAI figures it out automatically.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🏷️</div>
            <div class="feat-name">Names Preserved</div>
            <div class="feat-desc">Proper nouns, names, and brands handled correctly — "Deepak" stays "Deepak", not "गहरा".</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">⚡</div>
            <div class="feat-name">Instant Results</div>
            <div class="feat-desc">No model downloads, no warm-up time. Translations arrive in milliseconds.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🚀</div>
            <div class="feat-name">Deploy Anywhere</div>
            <div class="feat-desc">Lightweight — runs on Streamlit Cloud, Render, or Railway with zero GPU required.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class="site-footer">
    LinguaAI · Built with Streamlit & Google Translate · 100+ Languages · Deploy Anywhere for Free
</div>
""", unsafe_allow_html=True)

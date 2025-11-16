import streamlit as st
import base64
from pathlib import Path
import os

# ------------------------------------------------------
# BASE DIRECTORY (folder where app.py is located)
# ------------------------------------------------------
BASE_DIR = Path(__file__).parent
# ------------------------------------------------------
# LOAD CUSTOM CSS (robust version)
# ------------------------------------------------------
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).parent

# Try multiple possible file names
possible_styles = ["styles", "styles.css"]

STYLE_PATH = None
for filename in possible_styles:
    path = BASE_DIR / filename
    if path.exists():
        STYLE_PATH = path
        break

if STYLE_PATH:
    with open(STYLE_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error(
        "Could not load stylesheet. Make sure 'styles' or 'styles.css' "
        "is next to app.py."
    )

# ------------------------------------------------------
# TITLE
# ------------------------------------------------------
st.markdown("<h1>Harmoni – Wellness & Focus App</h1>", unsafe_allow_html=True)
st.write("Your personal space for calm, clarity, and emotional well-being.")

# ------------------------------------------------------
# GUIDEBOOK PDF SECTION
# ------------------------------------------------------
st.markdown("<h2>Your Guidebook</h2>", unsafe_allow_html=True)
st.write("Read the guide to understand focus, stress, and how to use Harmoni effectively.")

PDF_PATH = BASE_DIR / "Music_Emotions.pdf"

if PDF_PATH.exists():
    with open(PDF_PATH, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    st.markdown(
        f"""
        <div class="card">
            <embed src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" height="600px" type="application/pdf">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error(f"PDF '{PDF_PATH.name}' not found. Upload it to the app folder.")

# ------------------------------------------------------
# MUSIC PLAYER
# ------------------------------------------------------
st.markdown("<h2>Music Player</h2>", unsafe_allow_html=True)

MUSIC_FOLDER = BASE_DIR / "music"

if not MUSIC_FOLDER.exists():
    st.error("The 'music' folder is missing. Please create it and upload MP3 files.")
else:
    music_files = [f.name for f in MUSIC_FOLDER.glob("*.mp3")]
    if not music_files:
        st.warning("No MP3 files found in the music folder.")
    else:
        chosen_track = st.selectbox("Choose a track:", music_files)
        audio_path = MUSIC_FOLDER / chosen_track
        audio_bytes = open(audio_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")

# ------------------------------------------------------
# FEEDBACK SECTION
# ------------------------------------------------------
st.markdown("<h2>Session Feedback</h2>", unsafe_allow_html=True)
st.write("Your feedback helps improve Harmoni.")

with st.form("feedback_form"):
    feedback = st.text_area("How did you feel after your session?")
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    FEEDBACK_FILE = BASE_DIR / "feedback.txt"
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n---- Feedback Entry ----\n{feedback}\n")
    st.success("Your feedback has been recorded. Thank you!")

import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

# 1. Page Config
st.set_page_config(page_title="AI Crop Assistant", layout="wide", page_icon="🌾")

# Custom CSS for a clean "Hackathon" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2e7d32; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Translator
@st.cache_resource
def get_translator():
    return Translator()

translator = get_translator()

# Title and Logo (Logo prompt requirement)
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("AI Crop Assistant 🌾")
with col_logo:
    # Use a generic farm logo icon
    st.image("https://flaticon.com", width=100)

st.markdown("---")

# 2. Sidebar / Language Selection
language_map = {"English": "en", "Kannada": "kn", "Hindi": "hi"}
selected_lang = st.sidebar.selectbox("🌐 Select Language", list(language_map.keys()))
lang_code = language_map[selected_lang]

# 3. Layout: Two Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📥 Input Section")
    
    # Image Upload
    uploaded_file = st.file_uploader("Upload Crop Photo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    # Text Input (Analysis prompt requirement)
    problem_text = st.text_input("Describe the problem (e.g., yellow leaves, brown spots)", "").lower()
    
    analyze_btn = st.button("🚀 Analyze Crop")

with col2:
    st.header("🔍 Diagnosis & Solution")
    
    if analyze_btn:
        if not problem_text and not uploaded_file:
            st.error("⚠️ Please provide an image or describe the problem.")
        else:
            # Logic for Analysis (If-Else logic requirement)
            disease, cause, solution = "Healthy / Unknown", "No specific issues detected", "Keep monitoring the crop and ensure proper sunlight."
            
            if "yellow" in problem_text or "leaves" in problem_text:
                disease, cause, solution = "Nitrogen Deficiency", "Lack of essential nutrients in soil", "Apply Urea or nitrogen-rich fertilizer immediately."
            elif "brown" in problem_text or "spots" in problem_text:
                disease, cause, solution = "Fungal Infection", "Excess moisture or fungal spores", "Spray organic fungicide and reduce evening watering."
            elif "wilting" in problem_text or "dry" in problem_text:
                disease, cause, solution = "Water Stress", "Under-watering or extreme heat", "Increase irrigation frequency and check soil moisture."

            # Translation Logic (Multilingual requirement)
            try:
                t_disease = translator.translate(disease, dest=lang_code).text
                t_cause = translator.translate(cause, dest=lang_code).text
                t_sol = translator.translate(solution, dest=lang_code).text
                t_label_d = translator.translate("Disease", dest=lang_code).text
                t_label_c = translator.translate("Cause", dest=lang_code).text
                t_label_s = translator.translate("Solution", dest=lang_code).text
            except:
                t_disease, t_cause, t_sol = disease, cause, solution
                t_label_d, t_label_c, t_label_s = "Disease", "Cause", "Solution"

            # Display Output
            st.success(f"**{t_label_d}:** {t_disease}")
            st.info(f"**{t_label_c}:** {t_cause}")
            st.warning(f"**{t_label_s}:** {t_sol}")

            # 4. Text-to-Speech (TTS requirement)
            st.write("---")
            st.subheader("🔊 Listen to Solution")
            
            try:
                tts = gTTS(text=t_sol, lang=lang_code)
                filename = "temp_audio.mp3"
                tts.save(filename)
                st.audio(filename)
                # Remove file after playing to avoid errors
                os.remove(filename) 
            except Exception as e:
                st.error("Audio generation unavailable offline.")
    else:
        st.info("Waiting for analysis... Provide details on the left.")

# 5. Government Schemes Section (Schemes requirement)
st.markdown("---")
st.header("🏛️ Helpful Government Schemes")
schemes = [
    "✅ **PM-Kisan Samman Nidhi**: Financial support of ₹6,000/year.",
    "✅ **Pradhan Mantri Fasal Bima Yojana**: Crop insurance against natural calamities.",
    "✅ **Soil Health Card Scheme**: Get your soil tested for better yields."
]

for scheme in schemes:
    try:
        translated_scheme = translator.translate(scheme, dest=lang_code).text
        st.write(translated_scheme)
    except:
        st.write(scheme)
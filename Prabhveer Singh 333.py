# text2imgPS333_Advanced.py

import streamlit as st
import requests
import time
import base64
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter

# -------------------------------------------------------------------
# CUSTOM PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="PS333 Advanced Image Generator",
    page_icon="🔥",
    layout="centered",
)

# -------------------------------------------------------------------
# CUSTOM CSS FOR UI ENHANCEMENT
# -------------------------------------------------------------------
custom_css = """
<style>
body {
    background: #0f0f0f;
}
.main-title {
    text-align: center;
    font-size: 48px;
    color: #ffdd00;
    font-weight: bold;
}
.sub {
    text-align: center;
    font-size: 20px;
    color: #ffffffaa;
}
.stButton>button {
    border-radius: 10px;
    font-weight: bold;
    font-size: 20px;
    border: 2px solid #ffcc00;
}
.gallery-img {
    border-radius: 10px;
    margin: 10px;
    border: 2px solid #444;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------------------------------------------
# HEADER IMAGE + TITLE
# -------------------------------------------------------------------
st.image("https://i.ibb.co/hJVMdhNV/Photo-Fixer-Bot-aifaceswap-dac4ce0cdd00acf259c01808d4253130.jpg", width=230)
st.markdown('<p class="main-title">🔥 PS333 ADVANCED IMAGE GENERATOR 🔥</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">AI-Powered Ultimate Creation Studio</p>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# SESSION HISTORY INITIALIZATION
# -------------------------------------------------------------------
if "gallery" not in st.session_state:
    st.session_state.gallery = []

# -------------------------------------------------------------------
# SIDEBAR ADVANCED SETTINGS
# -------------------------------------------------------------------
st.sidebar.header("⚙️ Advanced Settings")

model = st.sidebar.selectbox(
    "AI Model",
    ["Pollinations AI", "Dreamlike Diffusion", "Cyberrealistic XL", "RealVis XL", "AnimeVision Turbo"]
)

style = st.sidebar.selectbox(
    "Image Style",
    ["Realistic", "Cartoon", "Fantasy", "Cyberpunk", "Anime", "Photorealistic", "Cinematic", "HDR", "Watercolor"]
)

size = st.sidebar.selectbox(
    "Image Resolution",
    ["512x512", "768x768", "1024x1024", "2048x2048"]
)

seed = st.sidebar.number_input("Random Seed (0 = auto)", min_value=0, max_value=999999, value=0)

sharp = st.sidebar.slider("Sharpness", 1.0, 3.0, 1.0)
contrast = st.sidebar.slider("Contrast", 1.0, 3.0, 1.0)
brightness = st.sidebar.slider("Brightness", 1.0, 3.0, 1.0)

negative_prompt = st.sidebar.text_area("Negative Prompt", placeholder="Things to avoid...")

theme = st.sidebar.radio("Theme Mode", ["Dark", "Light"])

if theme == "Light":
    st.write("""
        <style>
        body { background: #f5f5f5; }
        </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# MAIN INPUT FIELDS
# -------------------------------------------------------------------
prompt = st.text_input("✨ Enter your prompt", placeholder="E.g. A tiger meditating in a cyberpunk city")

if st.button("🚀 Generate Image", use_container_width=True):
    if prompt.strip() == "":
        st.warning("❗ Please enter a prompt.")
    else:
        with st.spinner("⏳ Generating your masterpiece, wait zra..."):
            time.sleep(1)

            # -------------------------------------------------------------------
            # FORMAT PROMPT FOR URL
            # -------------------------------------------------------------------
            formatted_prompt = f"{style} style {prompt}"
            if negative_prompt:
                formatted_prompt += f" --no {negative_prompt}"
            formatted_prompt = formatted_prompt.replace(" ", "%20")

            # -------------------------------------------------------------------
            # POLLINATIONS URL
            # -------------------------------------------------------------------
            image_url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?size={size}"
            if seed != 0:
                image_url += f"&seed={seed}"

            # -------------------------------------------------------------------
            # FETCH IMAGE
            # -------------------------------------------------------------------
            try:
                img_data = requests.get(image_url).content
                img = Image.open(BytesIO(img_data))

                # Enhancements
                if sharp != 1.0:
                    img = ImageEnhance.Sharpness(img).enhance(sharp)
                if contrast != 1.0:
                    img = ImageEnhance.Contrast(img).enhance(contrast)
                if brightness != 1.0:
                    img = ImageEnhance.Brightness(img).enhance(brightness)

                st.image(img, use_container_width=True, caption="Generated by PS333 AI")

                # Save to gallery
                st.session_state.gallery.append(img)

                st.success("🔥 Your image is ready!")

                # DOWNLOAD BUTTONS
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()

                st.download_button(
                    label="📥 Download PNG",
                    data=img_bytes,
                    file_name="ps333_image.png",
                    mime="image/png"
                )

                # JPG version
                buffered_jpg = BytesIO()
                img.convert("RGB").save(buffered_jpg, format="JPEG")
                st.download_button(
                    label="📥 Download JPG",
                    data=buffered_jpg.getvalue(),
                    file_name="ps333_image.jpg",
                    mime="image/jpeg"
                )

                st.markdown(f"🔗 **Full Image URL:** {image_url}")

            except Exception as e:
                st.error("⚠️ Failed to generate image. Try again later.")
                st.write(e)

# -------------------------------------------------------------------
# GALLERY SECTION
# -------------------------------------------------------------------
st.markdown("---")
st.subheader("🖼️ Your Generated Images Gallery")

if len(st.session_state.gallery) == 0:
    st.info("No images generated yet.")
else:
    cols = st.columns(3)
    idx = 0
    for image in st.session_state.gallery:
        with cols[idx % 3]:
            st.image(image, caption=f"Image {idx+1}", use_container_width=True)
        idx += 1

# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '🔧 Made with ❤️ by [**PS333**](https://instagram.com/prabhveersingh01) | 🚀 Powered by **PS333 AI Studio**'
)

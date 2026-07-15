import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configure Gemini API securely using Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("Snap & Simplify AI Tutor 📚")
st.write("Upload a picture of your textbook page and ask how you want it explained!")

# 2. Image Upload Option
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# 3. User Input for Language/Preference
user_instruction = st.text_input("How should I explain this? (e.g., 'বাংলায় বুঝিয়ে দাও')", value="Explain in simple terms")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # 4. Corrected model name (100% stable version)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("Simplify This ✨"):
        with st.spinner("AI is thinking..."):
            try:
                response = model.generate_content([user_instruction, image])
                st.success("Done!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
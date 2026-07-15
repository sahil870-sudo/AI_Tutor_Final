import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configure Gemini API (Using Streamlit Secrets so GitHub doesn't block it)
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
    
    # 4. Instruction for the AI
    prompt = f"""
    You are a very helpful and friendly tutor. Look at the educational image provided above. 
    Explain the topic shown in the image based on the student's request: "{user_instruction}".
    Make it extremely simple, easy to understand, and use real-world examples.
    """
    
    if st.button("Simplify This ✨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner("AI is thinking..."):
            response = model.generate_content([prompt, image])
            st.success("Done!")
            st.write(response.text)
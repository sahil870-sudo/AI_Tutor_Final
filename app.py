import streamlit as st
from groq import Groq
import base64

# 1. Initialize Groq Client using Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Snap & Simplify AI Tutor 📚")
st.write("Upload a picture of your textbook page and ask how you want it explained!")

# 2. Image Upload Option
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
user_instruction = st.text_input("How should I explain this? (e.g., 'বাংলায় বুঝিয়ে দাও')", value="Explain in simple terms")

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    # Convert image to base64 for Groq
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    if st.button("Simplify This ✨"):
        with st.spinner("AI is thinking..."):
            try:
                # Using Llama 3.2 90b Vision which is fast and completely free on Groq
                response = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"You are a helpful tutor. Explain this based on: {user_instruction}. Keep it very simple."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                )
                st.success("Done!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
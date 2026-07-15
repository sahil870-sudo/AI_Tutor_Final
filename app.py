import streamlit as st
from openai import OpenAI
from PIL import Image

# 1. Configure OpenAI API (Using Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    You are a very helpful and friendly tutor. Look at the educational image provided. 
    Explain the topic shown in the image based on the student's request: "{user_instruction}".
    Make it extremely simple, easy to understand, and use real-world examples.
    """
    
    if st.button("Simplify This ✨"):
        with st.spinner("AI is thinking..."):
            try:
                # Using GPT-4o mini which supports vision and is cost-effective
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{uploaded_file.getvalue().hex()}"
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
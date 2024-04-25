from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image, UserQuestion):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0],UserQuestion])
    return response.text
def input_image_setup(uploaded_file): 
    if uploaded_file is not None:
    #   Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
            "mime_type": uploaded_file.type,
            "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption ="Uploaded Image.", use_column_width=True)

submit = st.button("Get data from my extract")

Input_Prompt = """
    You are an expert in understanding invoices. you will receive
    input image as invoices and you will have to answer questions based
    on the input image
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(Input_Prompt,image_data, input)
    st.subheader("The answer for \"" + input + "\" is : ")
    st.write(response)
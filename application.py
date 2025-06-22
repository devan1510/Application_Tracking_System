from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
import tempfile
from docx import Document
from docx2pdf import convert
import pytesseract

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key = GOOGLE_API_KEY)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_gemini_response(input, content_data, prompt):
    llm_model = genai.GenerativeModel('gemini-1.5-flash')  # or gemini-1.5-pro
    content = content_data[0]['data']
    response = llm_model.generate_content([input, content, prompt])
    return response.text

def input_file_setup(uploaded_file):
    if not uploaded_file:
        raise FileNotFoundError("NO FILE UPLOADED")

    file_ext = uploaded_file.name.lower().split('.')[-1]

    if file_ext == 'pdf':
        pdf_bytes = uploaded_file.read()
        images = convert_from_bytes(pdf_bytes)
        extracted_text = ""
        for img in images:
            extracted_text += pytesseract.image_to_string(img)
        return [{
            "mime_type": "text/plain",
            "data": extracted_text
        }]

    elif file_ext == 'docx':
        doc = Document(uploaded_file)
        full_text = '\n'.join([para.text for para in doc.paragraphs])
        return [{
            "mime_type": "text/plain",
            "data": full_text
        }]

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")


# build the interface using streamlit
st.set_page_config(page_title = "MR. TECH Resume")
st.header("APPLICATION TRACKING SYSTEM")
input_text = st.text_area("Description of the Role you are applying for...")
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or Word format)",
    type=["pdf", "docx"]
)

if uploaded_file:
    st.write("document uploaded successfully")

submit1 = st.button("Get Resume Description")

submit2 = st.button("Get Recommendations for Resume Improvements")

submit3 = st.button("PERCENTAGE MATCH(document to job description)")

input_prompt1 = """You are a Human Resouce Manager with Experience in the field of 
Web Development,Big Data Engineering,Data Science, Backend Development,Data Science, 
Data Analysis, DEVOPS, MLOPS, Data Engineering.
your task is to review the provided resume document of a candidate who is applying for the given job description.
Please share your professional evaluation on whether the candidat's profile aligns with the given job description.
Highlight the strengths and weaknesses of the applicant in realtion to the specified requirements of the described role.
"""

input_prompt2 = """
You are a Human Resouce Manager with Experience in the field of 
Web Development,Big Data Engineering,Data Science, Backend Development,Data Science, 
Data Analysis, DEVOPS, MLOPS, Data Engineering.
You are tasked with making recommendation towards what skills the candidate is 
currently missing with respect to the job description.
Make sure you give the response in bullet points with a short description of each point.
"""

input_prompt3 = """
You are an skilled Application Tracking System scanner with a deep understanding
with a deep understanding Web Development,Big Data Engineering,Data Science, Backend Development,Data Science, 
Data Analysis, DEVOPS, MLOPS, Data Engineering and MOST IMPORTANTLY comprehensive Application Tracking System functionality.
your task is to evaluate the provided resume document against the provided job description. Give me the percentage
match of the resume to the job description.
"""

if submit1:
    if uploaded_file:
        pdf_content = input_file_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,
                                       pdf_content,
                                    input_text)
        st.subheader("the generated response is ...")
        st.write(response)
    else:
        st.write("PLEASE UPLOAD A DOCUMENT")
    
elif submit2:
    if uploaded_file:
        pdf_content = input_file_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,
                                       pdf_content,
                                    input_text)
        st.subheader("the generated response is ...")
        st.write(response)
    else:
        st.write("PLEASE UPLOAD A DOCUMENT")

elif submit3:
    if uploaded_file:
        pdf_content = input_file_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,
                                       pdf_content,
                                    input_text)
        st.subheader("the generated response is ...")
        st.write(response)
    else:
        st.write("PLEASE UPLOAD A DOCUMENT")

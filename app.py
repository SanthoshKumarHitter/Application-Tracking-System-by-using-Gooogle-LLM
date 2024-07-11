import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## Loading all the Environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Google Gemini Pro Response

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

##Prompt Template
input_prompt= """Act like a highly skilled and experienced ATS (Applicant Tracking System) with a deep understanding
           of the tech field, including roles such as Software Engineer, Data Scientist, Data Analyst, Big Data Engineer, 
           Your task is to evaluate the resume based on the given job description. 
           Considering the competitive job market, you should provide the best assistance for improving resumes. 
           Assign a percentage match based on the job description and identify the missing keywords with high accuracy.

  """

## Streamlit App

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        color: #4CAF50; /* Green */
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        color: #FFA500; /* Orange */
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        color: #FF5733; /* Red-Orange */
        font-size: 1.2em;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .result {
        color: #3498DB; /* Blue */
        font-size: 1.1em;
    }
    .error {
        color: #E74C3C; /* Red */
        font-size: 1.1em;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App
st.markdown('<div class="main-title">SmartHire</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Improve your Resume ATS Score</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
jd = st.text_area("Paste the Job Description here")

st.markdown('<div class="section-header">Resume Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner("Processing..."):
            resume_text = input_pdf_text(uploaded_file)
            full_prompt = input_prompt + "\nJob Description:\n" + jd + "\nResume Text:\n" + resume_text
            response = get_gemini_response(full_prompt)
        
        st.success("Processing Complete!")
        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="result">{}</div>'.format(response.replace("\n", "<br>")), unsafe_allow_html=True)
    else:
        st.markdown('<div class="error">Please provide both a job description and a resume.</div>', unsafe_allow_html=True)
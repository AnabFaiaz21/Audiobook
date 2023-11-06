from google.cloud import texttospeech
import streamlit as st
import PyPDF2
import os
import json 
from gtts import gTTS
#google_application_credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials

def pdf_to_text(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    extracted_text = ""

    for page_index in range(num_pages):
        page = pdf_reader.pages[page_index]
        page_text = page.extract_text()
        extracted_text += page_text
 
    return extracted_text.strip()

languages = ['en', 'de', 'fr', 'es']
def text_to_audio(text, languages=['en'], save_paths=None):
    if not text:
        print("No text to convert to audio.")
        return

    if save_paths is None:
        save_paths = ['output_{}.mp3'.format(lang) for lang in languages]

    for lang, save_path in zip(languages, save_paths):
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(save_path)
        st.audio(save_path, format='audio/mp3')
        print(f'Audiobook saved as {save_path}')
st.title("Audiobook Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("PDF file uploaded successfully!")

    # Extract text from the PDF
    extracted_text = pdf_to_text(uploaded_file)

    # Language selection
    language = st.selectbox("Select Language", ['en', 'de', 'fr', 'es'])

    # Gender selection
    gender = st.selectbox("Select Gender", ['neutral', 'male', 'female'])

    # Convert text to audio and display
    text_to_audio(extracted_text, languages=[language], save_paths=None)

from google.cloud import texttospeech
import streamlit as st
import PyPDF2
import os

# Retrieve API key from GitHub secrets
api_key = os.environ.get('api_key')

def pdf_to_text(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    extracted_text = ""

    for page_index in range(num_pages):
        page = pdf_reader.pages[page_index]
        page_text = page.extract_text()
        extracted_text += page_text

    return extracted_text.strip()

def text_to_audio(text, language='en', gender='neutral', save_path='output.mp3'):
    client = texttospeech.TextToSpeechClient(credentials=API_KEY)


    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language,
        ssml_gender=gender.upper() if gender in ['neutral', 'male', 'female'] else 'NEUTRAL',
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(save_path, "wb") as out_file:
        out_file.write(response.audio_content)

    st.audio(save_path, format="audio/mp3")

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
    text_to_audio(extracted_text, language=language, gender=gender)

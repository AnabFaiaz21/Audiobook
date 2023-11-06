import streamlit as st
import PyPDF2
from gtts import gTTS
from gender_guesser.detector import Detector
from googletrans import Translator



def pdf_to_text(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    extracted_text = ""

    for page_index in range(num_pages):
        page = pdf_reader.pages[page_index]
        page_text = page.extract_text()
        extracted_text += page_text

    return extracted_text.strip()


from translate import Translator

def translate_text(text, source_language='en', target_language='en'):
    translator = Translator(from_lang=source_language, to_lang=target_language)
    try:
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text



def text_to_audio(text, text_language='en', voice_language='en', voice='neutral', save_path='output.mp3'):
    if not text:
        print("No text to convert to audio.")
        return

    # Translate text if the source and target languages are different
    if text_language != voice_language:
        text = translate_text(text, source_language=text_language, target_language=voice_language)

    if voice == 'neutral':
        selected_voice_language = voice_language
    else:
        detector = Detector()
        detected_gender = detector.get_gender(text.split()[0])

        if detected_gender in ['male', 'female']:
            selected_voice_language = f'{detected_gender}_{voice_language}'
        else:
            selected_voice_language = voice_language

    tts = gTTS(text=text, lang=selected_voice_language, slow=False)
    tts.save(save_path)
    st.audio(save_path, format='audio/mp3')
    print(f'Audiobook saved as {save_path}')


st.title("Multilingual Audio book Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("PDF file uploaded successfully!")

    # Extract text from the PDF
    extracted_text = pdf_to_text(uploaded_file)

    # Text language selection
    text_language = st.selectbox("Select Text Language", ['en', 'de', 'fr', 'es'])

    # Voice (gender) language selection
    voice_language = st.selectbox("Select Voice Language", ['en', 'de', 'fr', 'es'])

    # Voice (gender) selection
    voice_options = ['neutral', 'male', 'female']
    voice = st.selectbox("Select Voice", voice_options)

    # Convert text to audio and display
    text_to_audio(extracted_text, text_language=text_language, voice_language=voice_language, voice=voice)

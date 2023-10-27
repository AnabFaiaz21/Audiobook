from gtts import gTTS
import PyPDF2

def pdf_to_text(pdf_path):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_path)

    # Get the total number of pages in the PDF file
    num_pages = len(pdf_reader.pages)

    # Initialize an empty string variable to store the extracted text
    extracted_text = ""

    # Loop through each page in the PDF file
    for page_index in range(num_pages):
        # Get the page object
        page = pdf_reader.pages[page_index]

        # Extract the text from the page
        page_text = page.extract_text()

        # Append the extracted text to the variable
        extracted_text += page_text

    return extracted_text

# Specify the languages you want to include
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
        print(f'Audiobook saved as {save_path}')
    pass


pdf_path = "D:\Portfolio projects\Audiobook\content.pdf"

extracted_text = pdf_to_text(pdf_path)
text_to_audio(extracted_text,languages=languages)

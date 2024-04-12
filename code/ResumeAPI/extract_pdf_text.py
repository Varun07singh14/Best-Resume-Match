import io
import re
from PyPDF2 import PdfReader


def extract_text_from_file(file):

    text_data = file.download_as_string()

    pdf_file = io.BytesIO(text_data)
    pdf_reader = PdfReader(pdf_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    #all_resume_texts.append(remove_unwanted_data_in_text(text))

    return remove_unwanted_data_in_text(text)


def remove_unwanted_data_in_text(text):
    filtered_text = re.sub(r'[^a-zA-Z\s]', '', text)
    filtered_text = re.sub(r'http\S+\s', '', filtered_text)
    filtered_text = re.sub(r'\s+', ' ', filtered_text)
    filtered_text = re.sub(r'@\S+', '', filtered_text)
    filtered_text = re.sub(r'#\S+', '', filtered_text)
    filtered_text = re.sub(r'â€¢', '', filtered_text)

    return filtered_text

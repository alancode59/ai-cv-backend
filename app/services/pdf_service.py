import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        for page in document:
            text += page.get_text()

    return text.strip()
import fitz
import re


class PDFServiceError(Exception):
    pass


MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def validate_pdf_file(file_bytes: bytes, content_type: str):
    if content_type != "application/pdf":
        raise PDFServiceError("Only PDF files are allowed")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise PDFServiceError(
            f"PDF file size must be less than {MAX_FILE_SIZE_MB} MB")


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:

            if document.is_encrypted:
                raise PDFServiceError(
                    "Password-protected PDFs are not supported")

            text = ""

            for page in document:
                text += page.get_text()

            text = clean_text(text)

            if not text or len(text) < 50:
                raise PDFServiceError("Could not extract enough text from PDF")

            return text

    except PDFServiceError:
        raise

    except Exception:
        raise PDFServiceError("Invalid or corrupted PDF file")

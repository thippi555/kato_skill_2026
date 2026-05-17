import io

import pdfplumber


class FileLoader:

    def load_pdf_text_from_bytes(self, pdf_binary: bytes):

        text = ""

        with pdfplumber.open(io.BytesIO(pdf_binary)) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text
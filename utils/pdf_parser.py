from io import BytesIO

import PyPDF2


async def parse_pdf(file):
    pdf_content = await file.read()
    pdf_file = BytesIO(pdf_content)

    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text.lower()  # Convert to lowercase for easier matching

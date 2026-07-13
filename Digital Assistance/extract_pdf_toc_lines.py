from pathlib import Path
from pypdf import PdfReader
import re

pdf_path = Path('uploaded_documents') / 'Internship Documentation.pdf'
reader = PdfReader(pdf_path)
text = '\n'.join((reader.pages[i].extract_text() or '') for i in range(min(5, len(reader.pages))))
lines = [line.strip() for line in text.splitlines() if line.strip()]
for line in lines:
    if re.match(r'^(Chapter \d+:|\d+\.\d+|\d+\.\d+\.\d+)', line, re.I) or 'Table of Contents' in line:
        print(line)
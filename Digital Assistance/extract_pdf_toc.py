from pathlib import Path
from pypdf import PdfReader

pdf_path = Path('uploaded_documents') / 'Internship Documentation.pdf'
reader = PdfReader(pdf_path)

if hasattr(reader, 'outline'):
    outlines = reader.outline
else:
    outlines = reader.get_outlines()


def print_outlines(items, depth=0):
    for item in items:
        if isinstance(item, list):
            print_outlines(item, depth + 1)
        else:
            title = getattr(item, 'title', str(item))
            print('  ' * depth + '- ' + title)

print('PDF path:', pdf_path.resolve())
print('Number of pages:', len(reader.pages))
print('Table of Contents:')
print_outlines(outlines)

from pathlib import Path
from pypdf import PdfReader

pdf_path = Path('uploaded_documents') / 'Internship Documentation.pdf'
reader = PdfReader(pdf_path)
text_pages = [page.extract_text() for page in reader.pages]
print('PDF path:', pdf_path.resolve())
print('Number of pages:', len(reader.pages))
print('\n=== FIRST PAGE TEXT ===')
print(text_pages[0][:1500] if text_pages[0] else '<no text>')

for i, text in enumerate(text_pages[:5], start=1):
    if text and 'contents' in text.lower():
        print(f'\n=== PAGE {i} CONTAINS "contents" ===')
        print(text[:2500])

print('\n=== SEARCH FOR TOC HEADINGS ===')
for i, text in enumerate(text_pages[:10], start=1):
    if not text:
        continue
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if any('contents' in line.lower() for line in lines):
        print(f'\nPAGE {i} LINES WITH contents:')
        for line in lines:
            if 'contents' in line.lower():
                print('  ' + line)
    if i <= 3:
        print(f'\nPAGE {i} FIRST 20 LINES:')
        for line in lines[:20]:
            print('  ' + line)

import pdfplumber
import sys

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\WIN\Desktop\New folder\NHCH_VXL_C1_NA.pdf'
try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f'Total pages: {len(pdf.pages)}\n')
        # Extract text from first 3 pages
        for i, page in enumerate(pdf.pages[:3]):
            print(f'=== PAGE {i+1} ===')
            text = page.extract_text()
            if text:
                print(text)
            print('\n' + '='*50 + '\n')
except Exception as e:
    print(f'Error: {e}')

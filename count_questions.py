import pdfplumber
import json
import re

pdf_path = r'C:\Users\WIN\Desktop\New folder\NHCH_VXL_C1_NA.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Save raw text for inspection
        with open(r'C:\Users\WIN\Desktop\New folder\raw_text.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        # Print statistics
        print(f"Total PDF pages: {len(pdf.pages)}")
        print(f"Total text length: {len(full_text)} characters")
        
        # Count questions
        q_count = len(re.findall(r'Câu\s+\d+', full_text))
        print(f"Questions found: {q_count}")
        
        # Show samples
        questions_found = re.findall(r'Câu\s+\d+', full_text)
        print(f"\nFirst 10 questions: {questions_found[:10]}")
        print(f"Last 10 questions: {questions_found[-10:]}")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

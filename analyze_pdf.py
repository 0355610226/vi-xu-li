import pdfplumber
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\WIN\Desktop\New folder\NHCH_VXL_C1_NA.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        # Extract ALL text from PDF
        full_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Save to file for analysis
        with open(r'C:\Users\WIN\Desktop\New folder\full_pdf_text.txt', 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        # Count questions
        q_matches = re.findall(r'Câu\s+\d+', full_text)
        print(f"Total 'Cau' markers found: {len(q_matches)}")
        
        # Get unique question numbers
        q_nums = sorted(set(int(m.split()[-1]) for m in q_matches if m.split()[-1].isdigit()))
        print(f"Unique question numbers: {len(q_nums)}")
        print(f"Range: {min(q_nums)} to {max(q_nums)}")
        
        missing = set(range(1, max(q_nums)+1)) - set(q_nums)
        if missing:
            print(f"Missing questions ({len(missing)}): {sorted(missing)}")
        else:
            print("All questions present!")
        
        print(f"\nFirst 10 question numbers: {q_nums[:10]}")
        print(f"Last 10 question numbers: {q_nums[-10:]}")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

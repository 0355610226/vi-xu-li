import pdfplumber
import json
import re

pdf_path = r'C:\Users\WIN\Desktop\New folder\NHCH_VXL_C1_NA.pdf'

questions = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from all pages
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Split by "Câu" pattern and parse
        parts = re.split(r'(?=Câu\s+\d+)', full_text)
        
        for part in parts:
            if not part.strip():
                continue
                
            # Extract question number
            match = re.match(r'Câu\s+(\d+)(?:\[<DE>\])?:\s*(.+?)(?=\[<\$>\])', part, re.DOTALL)
            if not match:
                continue
            
            q_num = match.group(1)
            question_text = match.group(2).strip()
            
            # Extract all options
            options = re.findall(r'\[<\$>\]\s*(.+?)(?=\[<\$>\]|$)', part, re.DOTALL)
            options = [opt.strip() for opt in options]
            
            if len(options) >= 4:
                questions.append({
                    "id": int(q_num),
                    "question": question_text,
                    "options": options[:4]
                })
        
        print(f"Total questions extracted: {len(questions)}\n")
        
        # Display first few questions
        for i, q in enumerate(questions[:5]):
            print(f"Câu {q['id']}: {q['question'][:100]}...")
            for j, opt in enumerate(q['options'][:4]):
                print(f"  {chr(65+j)}. {opt[:80]}...")
            print()
        
        # Save as JSON
        with open(r'C:\Users\WIN\Desktop\New folder\quiz_data.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(questions)} questions to quiz_data.json")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

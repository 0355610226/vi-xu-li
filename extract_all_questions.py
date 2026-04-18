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
        
        # Replace markers for easier parsing
        full_text = full_text.replace("[<$>]", "|OPT|")
        full_text = full_text.replace("[<DE>]", "")
        
        # Split by question pattern - look for "Câu" followed by number
        # Handle both "Câu1:" and "Câu 1:" formats
        questions_raw = re.split(r'(?=Câu\s*\d+)', full_text)
        
        for block in questions_raw:
            if not block.strip() or len(block) < 10:
                continue
            
            # Extract question number
            qmatch = re.match(r'Câu\s*(\d+)\s*(?:\[<DE>\])?\s*:\s*(.+?)(?=\|OPT\||$)', block, re.DOTALL)
            if not qmatch:
                continue
            
            q_id = int(qmatch.group(1))
            q_text = qmatch.group(2).strip()
            
            # Clean question text - remove extra spaces and newlines
            q_text = re.sub(r'\s+', ' ', q_text).strip()
            
            # Extract options after |OPT| markers
            options = re.split(r'\|OPT\|', block)
            options = options[1:] if len(options) > 1 else []
            
            clean_options = []
            for opt in options:
                opt = opt.strip()
                # Take only the first meaningful line/part
                opt = opt.split('\n')[0].split('Câu')[0] if 'Câu' in opt or '\n' in opt else opt
                # Clean whitespace
                opt = re.sub(r'\s+', ' ', opt).strip()
                opt = opt[:200]  # Limit length
                
                if opt and len(opt) > 2:
                    clean_options.append(opt)
            
            # Make sure we have at least 4 options
            if len(clean_options) >= 4:
                questions.append({
                    "id": q_id,
                    "question": q_text[:300],  # Limit question length
                    "options": clean_options[:4]
                })
        
        # Sort by question ID
        questions.sort(key=lambda x: x['id'])
        
        print(f"Total questions extracted: {len(questions)}")
        print(f"Question range: Cau {questions[0]['id']} to Cau {questions[-1]['id']}")
        
        # Display sample questions
        print("\n=== First 3 questions ===")
        for q in questions[:3]:
            print(f"\nCau {q['id']}: {q['question'][:80]}...")
            for j, opt in enumerate(q['options']):
                print(f"  {chr(65+j)}. {opt[:70]}...")
        
        print("\n=== Last 3 questions ===")
        for q in questions[-3:]:
            print(f"\nCau {q['id']}: {q['question'][:80]}...")
            for j, opt in enumerate(q['options']):
                print(f"  {chr(65+j)}. {opt[:70]}...")
        
        # Save to JSON
        with open(r'C:\Users\WIN\Desktop\New folder\all_questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(questions)} questions to all_questions.json")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

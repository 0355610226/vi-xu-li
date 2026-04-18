import pdfplumber
import re
import json

pdf_path = r'C:\Users\WIN\Desktop\New folder\NHCH_VXL_C1_NA.pdf'
questions = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Replace markers
        full_text = full_text.replace("[<$>]", "|OPT|")
        full_text = full_text.replace("[<DE>]", "")
        
        # Split questions - handle both "Câu1" and "Câu 1" formats
        questions_raw = re.split(r'(?=Câu\s*\d+)', full_text)
        
        for block in questions_raw:
            if not block.strip() or len(block) < 10:
                continue
            
            # Extract question number and text - handle both formats
            qmatch = re.match(r'Câu\s*(\d+)\s*:\s*(.+?)(?=\|OPT\||$)', block, re.DOTALL)
            if not qmatch:
                continue
            
            q_id = int(qmatch.group(1))
            q_text = qmatch.group(2).strip()
            
            # Clean question text
            q_text = re.sub(r'\s+', ' ', q_text).strip()
            q_text = q_text[:300]
            
            # Extract options
            options = re.split(r'\|OPT\|', block)
            options = options[1:] if len(options) > 1 else []
            
            clean_options = []
            for opt in options:
                opt = opt.strip()
                opt = opt.split('\n')[0].split('Câu')[0] if 'Câu' in opt or '\n' in opt else opt
                opt = re.sub(r'\s+', ' ', opt).strip()
                opt = opt[:200]
                
                if opt and len(opt) > 2:
                    clean_options.append(opt)
            
            if len(clean_options) >= 4:
                questions.append({
                    "id": q_id,
                    "question": q_text,
                    "options": clean_options[:4],
                    "correctAnswer": 0  # Placeholder - will be set manually
                })
        
        # Sort by ID
        questions.sort(key=lambda x: x['id'])
        
        print(f"Total questions extracted: {len(questions)}")
        if questions:
            print(f"Range: Cau {questions[0]['id']} to Cau {questions[-1]['id']}")
            print(f"\nFirst 3 questions:")
            for q in questions[:3]:
                print(f"  Cau {q['id']}: {q['question'][:60]}...")
            print(f"\nLast 3 questions:")
            for q in questions[-3:]:
                print(f"  Cau {q['id']}: {q['question'][:60]}...")
        
        # Save to JSON
        with open(r'C:\Users\WIN\Desktop\New folder\all_questions_with_answers.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved to all_questions_with_answers.json")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

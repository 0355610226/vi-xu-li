#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdfplumber
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_questions_from_pdf(pdf_path, chapter_num):
    """Extract all questions from PDF file"""
    questions = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Split by question markers - handle both "Câu \d+" and "Câu\d+"
            questions_raw = re.split(r'(?=Câu\d+:)', full_text)
            
            question_count = 0
            for block in questions_raw:
                if not block.strip():
                    continue
                    
                # Extract question number and text - match "Câu146:" format
                qmatch = re.match(r'Câu(\d+):\s*(.+?)(?=\[\<\$\>])', block, re.DOTALL)
                if not qmatch:
                    continue
                
                q_num = int(qmatch.group(1))
                q_text = qmatch.group(2).strip()
                
                # Extract options between [<$>] markers
                options = re.findall(r'\[\<\$\>\](.+?)(?=\[\<\$\>]|$)', block, re.DOTALL)
                
                if len(options) >= 4:
                    # Clean up options - remove newlines and extra spaces
                    clean_options = []
                    for opt in options[:4]:
                        cleaned = re.sub(r'\s+', ' ', opt.strip()).strip()
                        if cleaned:
                            clean_options.append(cleaned[:150])
                    
                    if len(clean_options) >= 4:
                        question_count += 1
                        questions.append({
                            "id": question_count,
                            "question": re.sub(r'\s+', ' ', q_text)[:300],
                            "options": clean_options[:4],
                            "correctAnswer": 0  # Placeholder - will be filled manually
                        })
            
            return questions
    
    except Exception as e:
        print(f"Lỗi khi xử lý {pdf_path}: {e}")
        return []

def main():
    chapters = [
        ("C2", r"C:\Users\WIN\Desktop\New folder\NHCH_VXL_C2_NA.pdf"),
        ("C3", r"C:\Users\WIN\Desktop\New folder\NHCH_VXL_C3_NA.pdf"),
        ("C4", r"C:\Users\WIN\Desktop\New folder\NHCH_VXL_C4_NA.pdf"),
    ]
    
    for chapter_name, pdf_path in chapters:
        print(f"\n{'='*50}")
        print(f"Extracting: {chapter_name}")
        print(f"{'='*50}")
        
        questions = extract_questions_from_pdf(pdf_path, chapter_name)
        
        if questions:
            output_file = rf"C:\Users\WIN\Desktop\New folder\quiz_{chapter_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Extracted {len(questions)} questions from Chapter {chapter_name}")
            print(f"✓ Saved to: quiz_{chapter_name}.json")
            print(f"First question: {questions[0]['question'][:60]}...")
            print(f"Last question: {questions[-1]['question'][:60]}...")
        else:
            print(f"✗ No questions found in {chapter_name}")

if __name__ == "__main__":
    main()

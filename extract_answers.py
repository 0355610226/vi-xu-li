import pdfplumber
import re
import json

pdf_path = r'C:\Users\WIN\Desktop\New folder\NGÂN-HÀNG-CÂU-HỎI-THI-TRẮC-NGHIỆM-chỉnh-sửa.pdf'
full_text = ''

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        full_text += (page.extract_text() or '') + '\n'

answers_dict = {}
questions = re.split(r'(?=Câu\s*\d+)', full_text)

for question in questions[1:]:
    match_num = re.search(r'Câu\s*(\d+)', question)
    if not match_num:
        continue
    q_num = int(match_num.group(1))
    
    # Find options marked with [<$>]
    options_with_marker = re.findall(r'\*?\[<\$>\]', question)
    correct_idx = -1
    for i, marker in enumerate(options_with_marker):
        if '*' in marker:
            correct_idx = i
            break
    
    answers_dict[q_num] = correct_idx

# Save to JSON
with open(r'C:\Users\WIN\Desktop\New folder\answers_key.json', 'w', encoding='utf-8') as f:
    json.dump(answers_dict, f, indent=2, ensure_ascii=False)

print(f'Successfully extracted {len(answers_dict)} answers!')
print(f'First 10 answers:')
for i in range(1, min(11, len(answers_dict) + 1)):
    print(f'  Câu {i}: {answers_dict.get(i, "N/A")}')

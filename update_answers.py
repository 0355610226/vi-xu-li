import json
import os

data_folder = r'C:\Users\WIN\Desktop\New folder'
quiz_folder = r'C:\Users\WIN\Desktop\quiz-deploy-all'

# Load all answers from PDF
with open(os.path.join(data_folder, 'answers_key.json'), 'r', encoding='utf-8') as f:
    all_answers = json.load(f)

# Map chapters to question ranges and file names
chapters = [
    {'name': 'C1', 'file': 'quiz_C1.json', 'range': (1, 145)},
    {'name': 'C2', 'file': 'quiz_C2.json', 'range': (146, 328)},
    {'name': 'C3', 'file': 'quiz_C3.json', 'range': (336, 435)},
    {'name': 'C4', 'file': 'quiz_C4.json', 'range': (436, 485)},
]

for chapter in chapters:
    file_path = os.path.join(quiz_folder, chapter['file'])
    start, end = chapter['range']
    
    # Load quiz file
    with open(file_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    # Update answers
    for i, question in enumerate(quiz_data):
        question_num = start + i
        if str(question_num) in all_answers:
            question['correctAnswer'] = all_answers[str(question_num)]
    
    # Save updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    
    print(f'Updated {chapter["name"]}: {chapter["file"]} (questions {start}-{end})')

print('All quiz files updated with correct answers!')

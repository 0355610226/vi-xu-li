import os
import re

# Define the HTML update logic
html_updates = {
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter1.html': {
        'json_file': 'quiz_C1.json',
        'questions_count': 145,
        'title': 'Bộ Trắc Nghiệm Vi Xử Lý - 145 Câu Hỏi'
    },
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter2.html': {
        'json_file': 'quiz_C2.json',
        'questions_count': 183,
        'title': 'Bộ Trắc Nghiệm Cấu Trúc Vi Xử Lý - 183 Câu Hỏi'
    },
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter3.html': {
        'json_file': 'quiz_C3.json',
        'questions_count': 99,
        'title': 'Bộ Trắc Nghiệm Lập Trình Hợp Ngữ - 99 Câu Hỏi'
    },
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter4.html': {
        'json_file': 'quiz_C4.json',
        'questions_count': 50,
        'title': 'Bộ Trắc Nghiệm Vi Điều Khiển 8051 - 50 Câu Hỏi'
    }
}

for html_file_path, config in html_updates.items():
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the json file name
    content = re.sub(
        r"fetch\('complete_quiz_\d+_questions\.json'\)",
        f"fetch('{config['json_file']}')",
        content
    )
    content = re.sub(
        r"fetch\('quiz_C[1-4]\.json'\)",
        f"fetch('{config['json_file']}')",
        content
    )
    
    # Update question count references
    old_count_patterns = [r"Câu \$\{currentQuestion \+ 1\}/\d+", r"/145", r"/183", r"/99", r"/50"]
    for pattern in old_count_patterns:
        if re.search(pattern, content):
            content = re.sub(
                r"Câu \$\{currentQuestion \+ 1\}/\d+",
                f"Câu ${{currentQuestion + 1}}/{config['questions_count']}",
                content
            )
            content = content.replace(f"/{145}", f"/{config['questions_count']}")
            content = content.replace(f"/{183}", f"/{config['questions_count']}")
            content = content.replace(f"/{99}", f"/{config['questions_count']}")
            content = content.replace(f"/{50}", f"/{config['questions_count']}")
    
    # Add the "show wrong answers only" feature in the results section
    # First, find the answer-review div and add a new section for wrong answers only
    
    # Find the section with "Xem lại các câu trả lời:" and add buttons to filter
    if 'Xem lại các câu trả lời:' in content:
        new_review_section = '''
            <div id="answer-review-controls" style="margin-bottom: 20px; display: flex; gap: 10px;">
                <button class="review-btn" onclick="showAllAnswers()" style="padding: 10px 20px; cursor: pointer; background: #667eea; color: white; border: none; border-radius: 5px; font-weight: bold;" id="btn-all">📋 Xem Tất Cả</button>
                <button class="review-btn" onclick="showWrongAnswersOnly()" style="padding: 10px 20px; cursor: pointer; background: #f44336; color: white; border: none; border-radius: 5px; font-weight: bold;" id="btn-wrong">❌ Chỉ Câu Sai</button>
            </div>
        '''
        
        # Insert the new controls before the answer-review
        if '<div class="answer-review" id="answer-review">' in content:
            content = content.replace(
                '<div class="answer-review" id="answer-review">',
                new_review_section + '<div class="answer-review" id="answer-review">'
            )
    
    # Now add the JavaScript functions to show/hide wrong answers
    # Find the end of the showResults function and add new functions after it
    
    # Add new JavaScript functions before the closing script tag
    new_functions = '''
        function showAllAnswers() {
            document.getElementById('btn-all').style.background = '#667eea';
            document.getElementById('btn-wrong').style.background = '#ccc';
            document.querySelectorAll('.answer-item').forEach(item => {
                item.style.display = 'block';
            });
        }

        function showWrongAnswersOnly() {
            document.getElementById('btn-all').style.background = '#ccc';
            document.getElementById('btn-wrong').style.background = '#f44336';
            document.querySelectorAll('.answer-item').forEach(item => {
                if (item.classList.contains('wrong')) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
'''
    
    # Insert before the closing script tag
    content = content.replace(
        '        // Load quiz when page loads',
        new_functions + '\n        // Load quiz when page loads'
    )
    
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Updated {os.path.basename(html_file_path)}')

print('All HTML files updated with wrong answers filter!')

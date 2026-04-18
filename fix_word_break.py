import os

# Add comprehensive word-breaking CSS to all chapter files
chapters = [
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter2.html',
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter3.html',
    r'C:\Users\WIN\Desktop\quiz-deploy-all\chapter4.html',
]

additional_css = '''
        /* Force word breaking */
        * {
            word-break: break-word;
            overflow-wrap: break-word;
        }
        
        .option {
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 15px;
        }
        
        button {
            word-break: break-word;
        }
'''

for filepath in chapters:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert CSS - after existing style definitions
    # Look for the closing </style> tag and insert before it
    if '</style>' in content:
        content = content.replace('</style>', additional_css + '\n    </style>', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Updated {os.path.basename(filepath)} with enhanced word-breaking CSS')

print('Done!')

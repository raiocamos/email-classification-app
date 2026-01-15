from flask import Flask, render_template, request
from backend import classify_email, extract_text_from_file
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    email_content = ""
    
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            email_content = extract_text_from_file(file)
            
    subject_input = request.form.get('email_subject', '').strip()
    body_input = request.form.get('email_text', '').strip()
    
    if body_input:
        if subject_input:
            email_content = f"Assunto: {subject_input}\n\n{body_input}"
        else:
            email_content = body_input
        
    if not email_content:
        return render_template('index.html', result=None, error="Por favor, forneça o conteúdo do email.")

    result = classify_email(email_content)
    
    return render_template(
        'index.html', 
        result=result, 
        email_subject=subject_input,
        email_body=body_input,
        email_text=email_content
    )

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import threading
from script_generator import *
from text_to_speech import *
from caption_generator import *
from video_processing import *
from utils import *
from PyPDF2 import PdfReader

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variable to track video processing status
video_status = {'status': 'idle', 'output_path': None}

def process_pdf(pdf_file_path):
    global video_status
    video_status['status'] = 'processing'
    
    print("Extracting text from PDF file...")
    reader = PdfReader(pdf_file_path)
    page_texts = []
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        page_texts.append(page.extract_text())
    pdf_text = "\n\n".join(page_texts)
    print("Text extracted")
    
    script = generate_script("script.txt", pdf_text)
    cleanedScript = remove_enclosed_words(script)
    voiceOver = create_voice_over("voiceOver.wav", cleanedScript) 
    result = generate_captions(voiceOver)
    text_lines = generate_text_lines(result, "background.mp4")
    delete_folder_contents("frames")
    folder_path, fps = extract_frames("background.mp4", "voiceOver.wav", "frames", text_lines)
    output_path = "static/output.mp4"
    compiling_output(folder_path, "voiceOver.wav", output_path, fps)
    delete_folder_contents("frames")
    
    video_status['status'] = 'complete'
    video_status['output_path'] = output_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global video_status
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            video_status = {'status': 'processing', 'output_path': None}
            threading.Thread(target=process_pdf, args=(file_path,)).start()
            return render_template('result.html')
    return render_template('upload.html')

@app.route('/status')
def get_status():
    return jsonify(video_status)

if __name__ == '__main__':
    app.run(debug=True)
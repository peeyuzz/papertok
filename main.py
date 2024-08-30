from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os
import shutil
from script_generator import *
from text_to_speech import *
from caption_generator import *
from video_processing import *
from utils import *
from PyPDF2 import PdfReader

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure the upload and output folders exist
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Global variable to track video processing status
video_status = {'status': 'idle', 'output_path': None}

def process_pdf(pdf_file_path: str):
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
    output_path = os.path.join(OUTPUT_FOLDER, "output.mp4")
    compiling_output(folder_path, "voiceOver.wav", output_path, fps)
    delete_folder_contents("frames")
    
    video_status['status'] = 'complete'
    video_status['output_path'] = '/static/output/output.mp4'

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    background_tasks.add_task(process_pdf, file_path)
    return {"filename": file.filename, "status": "Processing"}

@app.get("/status")
async def get_status():
    return JSONResponse(content=video_status)

@app.get("/result", response_class=HTMLResponse)
async def get_result(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
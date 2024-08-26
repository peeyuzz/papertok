from script_generator import *
from text_to_speech import *
from caption_generator import *
from video_processing import *
from utils import *

from PyPDF2 import PdfReader

def main():
    pdf_file_path = "pdfs/attentionisallyouneed.pdf"
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

    compiling_output(folder_path, "voiceOver.wav", "output.mp4", fps)

    delete_folder_contents("frames")

if __name__ == "__main__":
    main()
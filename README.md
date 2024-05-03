# PaperTok

PaperTok is a Python project that converts research papers into engaging TikTok videos, making it easier to understand and share complex academic content on social media platforms.

## Description

PaperTok takes a PDF file of a research paper as input and generates TikTok videos explaining the paper's key points, findings, and conclusions. The project leverages several Python libraries to accomplish this task:

- **PyPDF2**: Used to read and extract text from the input PDF file.
- **Gemini**: A natural language processing library used to generate a concise and engaging script for the video based on the extracted text.
- **pyttsx3**: A text-to-speech library used to generate voiceovers for the videos.
- **MoviePy**: A Python library for video editing, which is used to create the final TikTok videos by combining the voiceover with visuals and animations.

## Installation

1. Clone the repository:
   ```git clone https://github.com/your-username/papertok.git```
2. Navigate to the project directory:
   ```cd papertok```
3. Install the required dependencies:
   ```pip install -r requirements.txt```

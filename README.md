# PaperTok: PDF to TikTok Video Generator

PaperTok is a web application that converts PDF content into engaging TikTok-style videos. It automates the process of content extraction, script generation, and video creation, making it easy to transform academic papers, stories, or any PDF document into shareable short-form videos.

## Features

- PDF content extraction
- AI-powered script generation
- Text-to-speech conversion
- Automatic video creation with captions
- Web interface for easy uploads and downloads

## Prerequisites

- Python 3.7+
- FFmpeg
- Gemini API

### Installing FFmpeg

FFmpeg is required for video processing. Follow these instructions to install it:

#### On Windows:
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the downloaded archive
3. Add the FFmpeg `bin` folder to your system PATH

#### On macOS (using Homebrew):
```
brew install ffmpeg
```

#### On Linux (Ubuntu/Debian):
```
sudo apt update
sudo apt install ffmpeg
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/papertok.git
   cd papertok
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the necessary Gemini API key and configurations

## Usage

1. Start the web application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload a PDF file and follow the on-screen instructions to generate your TikTok video

## Project Structure

- `app.py`: Main Flask application
- `caption_generator.py`: Generates captions for the video
- `script_generator.py`: AI-powered script generation from PDF content
- `text_to_speech.py`: Converts generated script to speech
- `video_processing.py`: Handles video creation and editing
- `utils.py`: Utility functions
- `templates/`: HTML templates for the web interface
- `static/`: Static assets (CSS, JS, images)
- `uploads/`: Temporary storage for uploaded PDFs
- `frames/`: Temporary storage for video frames
- `pdfs/`: Storage for processed PDF files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

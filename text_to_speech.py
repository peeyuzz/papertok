from gtts import gTTS

def create_voice_over(fileName, text):
    if not text.strip():
        print("Error: The text input is empty.")
        return None
    
    try:
        print("Creating voiceover...")
        tts = gTTS(text)
        tts.save(fileName)
        print(f"Voiceover saved to {fileName}")
        return fileName
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


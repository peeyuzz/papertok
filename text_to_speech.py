import pyttsx3

def create_voice_over(fileName, text):
    print("Creating voiceover...")
    engine = pyttsx3.init()
    engine.save_to_file(text, fileName)
    engine.runAndWait()
    print(f"Voiceover saved to {fileName}")
    return fileName
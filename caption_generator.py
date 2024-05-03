import whisper
import cv2

def generate_captions(audio_file):
    print("Transcribing audio...")
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file, verbose = False, language = "en")
    print("Audio transcribed")
    return result

def generate_lines(text, start, end, fps, width, char_width):
    print("Generating lines...")
    lines = []
    total_frames = int((end - start) * fps)
    start_frame = int(start * fps)
    total_chars = len(text)
    words = text.split()

    current_line = ""
    line_start_frame = start_frame
    line_length = 0

    for word in words:
        word_length = (len(word) + 1) * char_width
        if line_length + word_length <= width:
            current_line += word + " "
            line_length += word_length
        else:
            line_end_frame = line_start_frame + int(line_length / char_width * total_frames / total_chars)
            lines.append([current_line.strip(), line_start_frame, line_end_frame])
            current_line = word + " "
            line_start_frame = line_end_frame
            line_length = word_length

    if current_line:
        line_end_frame = start_frame + total_frames
        lines.append([current_line, line_start_frame, line_end_frame])

    print("Lines generated")
    return lines

def generate_text_lines(result, video_file):
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.8
    FONT_THICKNESS = 2

    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    asp = 16/9

    ret, frame = cap.read()
    width = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)].shape[1]
    width = width - (width * 0.1)
    fps = cap.get(cv2.CAP_PROP_FPS)

    temp_text = result["segments"][0]["text"]
    temp_textsize = cv2.getTextSize(temp_text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
    char_width = int(temp_textsize[0] / len(temp_text))

    text_lines = []
    for i in result["segments"]:
        lines = generate_lines(i["text"], i["start"], i["end"], fps, width, char_width)
        text_lines.extend(lines)
    cap.release()
    return text_lines
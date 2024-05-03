import cv2
from moviepy.editor import *

def extract_frames(video_file, audio_file, folder_path,text_lines):
    print("Extracting frames...")
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    asp = width / height
    fps = cap.get(cv2.CAP_PROP_FPS)
    N_frames = 0
    audio_clip = AudioFileClip(audio_file)
    max_frames = audio_clip.duration * fps
    while N_frames <= max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]
        for i in text_lines:
            text = i[0]
            if N_frames >= i[1] and N_frames <= i[2]:
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                text_x = int((frame.shape[1] - text_size[0]) / 2)
                text_y = int(height/2)
                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255, 255), 2)
                break
        cv2.imwrite(os.path.join(folder_path, str(N_frames) + ".jpg"), frame)
        N_frames += 1
    print(f"Frames extracted to {folder_path}")
    return folder_path, fps

def compiling_output(folder_path, audio_file, output_path, fps):
    print("Compiling output video...")
    images = [img for img in os.listdir(folder_path) if img.endswith(".jpg")]
    images.sort(key=lambda x: int(x.split(".")[0]))

    frame = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = frame.shape

    clip = ImageSequenceClip([os.path.join(folder_path, image) for image in images], fps = fps)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path)
    print(f"Output saved to {output_path}")
import os
import shutil
import re

def remove_enclosed_words(script):
    # Remove text enclosed in double asterisks
    script = re.sub(r'\*\*(.*?)\*\*', '', script)
    # Remove text enclosed in brackets (e.g., [text])
    script = re.sub(r'\[.*?\]', '', script)
    # Remove emojis (this regex captures a wide range of emojis)
    script = re.sub(r'[^\w\s,]', '', script)
    return script

def delete_folder_contents(folder_path):
  print(f"Deleting all files in {folder_path}")
  for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      try:
          if os.path.isfile(file_path):
              os.remove(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
              print(f"Deleted directory and its contents: {file_path}")
      except Exception as e:
          print(f"Error deleting {file_path}: {e}")

  if not os.listdir(folder_path):
      print("All contents of folder have been deleted.")
  else:
      print("Some contents of could not be deleted.")
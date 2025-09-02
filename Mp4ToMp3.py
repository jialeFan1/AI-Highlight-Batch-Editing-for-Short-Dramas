import os
from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(video_folder, audio_folder):
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    for file_name in os.listdir(video_folder):
        if file_name.endswith('.mp4'):
            video_path = os.path.join(video_folder, file_name)
            audio_path = os.path.join(audio_folder, os.path.splitext(file_name)[0] + '.mp3')

            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path)
            video_clip.close()
            print(f"Converted {video_path} to {audio_path}")

if __name__ == "__main__":
    video_folder = "path/to/your/video/folder"
    audio_folder = "path/to/your/audio/folder"
    convert_mp4_to_mp3(video_folder, audio_folder)

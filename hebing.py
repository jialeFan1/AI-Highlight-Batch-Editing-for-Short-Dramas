import os
import json
from moviepy.editor import VideoFileClip
#5

# 定义文件夹路径
video_folder = 'video_folder'  # 替换为你的video_folder路径
highlight_scripts_folder = 'highlight_scripts'  # 替换为你的highlight_scripts文件夹路径
output_folder = 'shipinpianduan'  # 替换为你的输出文件夹路径

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_highlight_file(highlight_file):
    highlight_path = os.path.join(highlight_scripts_folder, highlight_file)
    with open(highlight_path, 'r', encoding='utf-8') as file:
        highlights = json.load(file)

    video_cache = {}

    base_name = os.path.splitext(highlight_file)[0]  # 去掉txt文件的扩展名
    file_output_folder = os.path.join(output_folder, base_name)

    if not os.path.exists(file_output_folder):
        os.makedirs(file_output_folder)

    for highlight in highlights:
        file_name = highlight['file_name']
        highlight_segments = highlight['highlight_segments']

        video_path = os.path.join(video_folder, file_name)

        if file_name not in video_cache:
            video_cache[file_name] = VideoFileClip(video_path)

        video_clip = video_cache[file_name]

        for idx, segment in enumerate(highlight_segments):
            start_time = segment['start_time']
            end_time = segment['end_time']
            print(f"Processing segment {start_time}-{end_time} from {file_name}")

            clip = video_clip.subclip(start_time, end_time)
            segment_output_path = os.path.join(file_output_folder, f"{base_name}_segment_{idx + 1}.mp4")

            try:
                clip.write_videofile(segment_output_path, codec="libx264")
                print(f"Saved segment {idx + 1} of {file_name} to {segment_output_path}")
            except Exception as e:
                print(f"Error processing segment {start_time}-{end_time} from {file_name}: {e}")

            clip.close()  # 手动关闭FFMPEG进程

if __name__ == '__main__':
    # 读取highlight_scripts文件夹中的文件
    highlight_files = [f for f in os.listdir(highlight_scripts_folder) if f.endswith('.txt')]

    for highlight_file in highlight_files:
        process_highlight_file(highlight_file)

    print("All segments have been successfully extracted and saved.")

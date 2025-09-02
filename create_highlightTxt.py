import os
import json
from openai import OpenAI

# 设置OpenAI API密钥
api_key = "yourkeyyy"
client = OpenAI(api_key=api_key)

def process_transcript(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript = json.load(file)
        return transcript
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def generate_highlight_script(transcript):
    prompt = f"""
Here are the script segments from various videos:
{json.dumps(transcript, ensure_ascii=False)}

Your task is to identify a story that can grab viewers' attention and make them want to continue watching. Combine segments into larger coherent scenes. The combined segments should form a logical story or sequence that creates intrigue or suspense. Aim to select segments that provide context, build tension, or present a cliffhanger. Ensure each segment is substantial enough to convey what is happening, rather than being too short. The total duration of all selected segments should add up to about 3 minutes, and notice the story you combined together must be like a short story that people can understand what is happening.

Provide the file name and the time segments for each highlight clip only, ensuring that the selected scenes form a cohesive and engaging narrative. Format the output as follows:
Important: only the file_name and time. no other words.
Example output format:

[
  {{"file_name": "01.mp4", "highlight_segments": [{{"start_time": 1, "end_time": 30}}, {{"start_time": 60, "end_time": 90}}]}},
  {{"file_name": "02.mp4", "highlight_segments": [{{"start_time": 80, "end_time": 140}}]}},
  {{"file_name": "03.mp4", "highlight_segments": [{{"start_time": 49, "end_time": 79}}]}},
  {{"file_name": "05.mp4", "highlight_segments": [{{"start_time": 52.06, "end_time": 82.42}}]}},
  {{"file_name": "07.mp4", "highlight_segments": [{{"start_time": 9, "end_time": 59.6}}]}},
  {{"file_name": "09.mp4", "highlight_segments": [{{"start_time": 38.54, "end_time": 79.2}}]}}
]

Identify and provide the highlight segments, ensuring they form a logical, suspenseful story and are substantial enough to represent significant events.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            n=1
        )
        highlight_script = response.choices[0].message.content
        return highlight_script
    except Exception as e:
        print(f"Error generating highlight script: {e}")
        return None

def save_highlight_script(highlight_script, output_path):
    if "[" in highlight_script and "]" in highlight_script:
        start_index = highlight_script.find("[")
        end_index = highlight_script.rfind("]") + 1
        highlight_script = highlight_script[start_index:end_index]
    else:
        print(f"File format incorrect for script: {highlight_script}")
        return

    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(highlight_script)
        print(f"Saved highlight script to {output_path}")
    except Exception as e:
        print(f"Error saving file {output_path}: {e}")

if __name__ == "__main__":
    transcript_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\SplitedByToken"
    output_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\highlight_scripts"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(transcript_folder):
        file_path = os.path.join(transcript_folder, file_name)
        if os.path.isfile(file_path):
            transcript = process_transcript(file_path)
            if transcript:
                highlight_script = generate_highlight_script(transcript)
                if highlight_script:
                    output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_highlight_script.txt")
                    save_highlight_script(highlight_script, output_path)

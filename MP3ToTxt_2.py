import os
import openai
from moviepy.editor import VideoFileClip
import requests
import json

# Set OpenAI's API key
openai.api_key = "sk-proj-ueNmf4t6ogSHSCOjrx5rT3BlbkFJfnnqPOPJUeJe2TpuhUZo"

def extract_audio_from_videos(video_folder, audio_folder):
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    for video_file in os.listdir(video_folder):
        if video_file.endswith(".mp4"):
            audio_path = os.path.join(audio_folder, os.path.splitext(video_file)[0] + ".mp3")
            if os.path.exists(audio_path):
                print(f"Audio file {audio_path} already exists. Skipping extraction.")
                continue

            video_path = os.path.join(video_folder, video_file)
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, codec='mp3')
            print(f"Extracted audio from {video_file} to {audio_path}")

def transcribe_audio_to_text(audio_folder, video_folder, transcript_folder):
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)

    transcripts = []

    for file_name in os.listdir(audio_folder):
        if file_name.endswith('.mp3'):
            audio_path = os.path.join(audio_folder, file_name)
            video_file = os.path.splitext(file_name)[0] + '.mp4'

            with open(audio_path, "rb") as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={
                        "Authorization": f"Bearer {openai.api_key}",
                    },
                    files={
                        "file": audio_file
                    },
                    data={
                        "model": "whisper-1",
                        "response_format": "verbose_json"
                    }
                ).json()

            # Print full response for debugging
            print(f"API response for {audio_path}: {response}")

            if "segments" in response:
                transcript_data = {
                    "file_name": video_file,
                    "segments": []
                }
                previous_end = None
                for segment in response["segments"]:
                    start_time = max(0, segment["start"] - 0.1)  # subtract 0.1 seconds for the start time
                    end_time = segment["end"] + 0.1  # add 0.1 seconds for the end time
                    text = segment["text"]

                    if previous_end is not None and start_time - previous_end <= 1:
                        # Merge with the previous segment
                        transcript_data["segments"][-1]["end_time"] = end_time
                        transcript_data["segments"][-1]["text"] += " " + text
                    else:
                        # Add as a new segment
                        transcript_data["segments"].append({
                            "start_time": start_time,
                            "end_time": end_time,
                            "text": text
                        })
                    previous_end = end_time

                transcripts.append(transcript_data)
                print(f"Transcribed {audio_path}")

            else:
                print(f"Error: 'segments' key not found in the response for {audio_path}")

    # Save the transcript data as a JSON file without spaces
    json_output_path = os.path.join(transcript_folder, "transcripts.json")
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(transcripts, json_file, ensure_ascii=False, separators=(',', ':'))

    print(f"Saved transcripts to {json_output_path}")

if __name__ == "__main__":
    video_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\video_folder"
    audio_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\audio_folder"
    transcript_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\transcripts"

    extract_audio_from_videos(video_folder, audio_folder)
    transcribe_audio_to_text(audio_folder, video_folder, transcript_folder)

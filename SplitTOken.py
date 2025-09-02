import os
import json
import tiktoken
#2

def load_transcripts(transcript_folder):
    json_path = os.path.join(transcript_folder, "transcripts.json")
    with open(json_path, 'r', encoding='utf-8') as file:
        transcripts = json.load(file)
    return transcripts

def split_transcripts(transcripts, output_folder, token_limit=25000):
    tokenizer = tiktoken.get_encoding("gpt2")
    current_tokens = 0
    file_index = 1
    split_transcripts = []

    for transcript in transcripts:
        transcript_tokens = len(tokenizer.encode(json.dumps(transcript, ensure_ascii=False)))
        if current_tokens + transcript_tokens > token_limit:
            # Save the current split_transcripts to a file
            output_path = os.path.join(output_folder, f"transcripts_part_{file_index}.json")
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(split_transcripts, json_file, ensure_ascii=False, separators=(',', ':'))
            print(f"Saved transcripts to {output_path}")

            # Reset for the next file
            split_transcripts = []
            current_tokens = 0
            file_index += 1

        split_transcripts.append(transcript)
        current_tokens += transcript_tokens

    # Save any remaining transcripts to a final file
    if split_transcripts:
        output_path = os.path.join(output_folder, f"transcripts_part_{file_index}.json")
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(split_transcripts, json_file, ensure_ascii=False, separators=(',', ':'))
        print(f"Saved transcripts to {output_path}")

if __name__ == "__main__":
    transcript_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\transcripts"
    output_folder = "C:\\Users\\jiale\\IdeaProjects\\ShiPinJianJi\\highlight_project\\scripts\\SplitedByToken"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    transcripts = load_transcripts(transcript_folder)
    split_transcripts(transcripts, output_folder, token_limit=10000)

import sys
import os
from typing import List, Tuple
from collections import namedtuple
import requests
import json
from tqdm import tqdm

# file name, dialogue text
DialogueLine = Tuple[str, str]

# In the skyrim creation kit, you can export all the dialogue for an NPC voice.
# The result is a text file separated by columns deliminated by a tab character.
# The relevant columns for us are the file path so we can have the expected file name for the audio file
# and the actual dialogue response text that the NPC will voice out.
# esp_name allows an easy way to only take dialogue lines from a particular plugin
# so we can ignore all of the vanilla lines from an NPC voice and only replace the lines from the plugin.
def parse_exported_dialogue_file(path: str, esp_name: str = '') -> List[DialogueLine]:
    FILE_PATH_COL = 15
    DIALOGUE_RESPONSE_TEXT = 20

    lines = []
    with open(path, "r", encoding="cp1252") as file:
        # skip header line
        next(file)

        for line in file:
            cols = line.split('	')

            path = cols[FILE_PATH_COL]
            if esp_name not in path:
                continue

            filename = path.split("\\")[-1]
            lines.append((filename, cols[DIALOGUE_RESPONSE_TEXT]))

    return lines

url = "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>"
headers = {
  'xi-api-key': '<key>',
  'Content-Type': 'application/json'
}

def get_voice_file_for_line(filename: str, text: str, output_folder: str):
    payload = json.dumps({
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 1
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    no_ext = os.path.splitext(filename)[0]
    with open(f"{output_folder}/{no_ext}.wav", "wb") as f:
        f.write(response.content)

def main():
    if len(sys.argv) > 1:
        esp_name = sys.argv[1]
    else:
        esp_name = ""
    
    output_folder = f"./ai_dialogue"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    lines = parse_exported_dialogue_file("export.txt", esp_name)
    for filename, text in tqdm(lines, ascii=True):
        get_voice_file_for_line(filename, text, output_folder)

main()
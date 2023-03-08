import sys
import os
import io
import requests
import json
import subprocess
from typing import List, Tuple, Dict
from collections import namedtuple
from tqdm import tqdm
from pydub import AudioSegment

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

# Returns true when successfully downloads and converts file.
# Returns false when download failed, most likely due to running out of credits.
def get_voice_file_for_line(url: str, headers: Dict[str, str], filename: str, text: str, output_folder: str) -> bool:
    payload = json.dumps({
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 1
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Error received from Elevenlabs API, most likely ran out of credits. Proceeding with what we have.")
        return False

    output_path = f"{output_folder}/{filename}" 

    # Elevenlabs returns an mp3 file in raw bytes
    # Convert it into wav in-memory
    audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")

    # Bethesda audio files have to be 16-bit WAV files, Mono, and at 44100Hz.
    audio.set_channels(1)
    audio.set_frame_rate(44100)
    audio.set_sample_width(2)

    audio.export(output_path, format="wav")

# Currently the best method I can find to generate lip files is to use FaceFXWrapper externally.
# Users will have to download on their own and drag the exe and FonixData.cdf into this folder.
def generate_lip_file(filename: str, text: str, output_folder: str):
    no_ext = os.path.splitext(filename)[0]
    process = subprocess.run([".\\FaceFXWrapper.exe", "Skyrim", "USEnglish", "FonixData.cdf", f"{output_folder}/{no_ext}.wav", f"{output_folder}/{no_ext}.lip", text], stdout=subprocess.DEVNULL)
    if process.returncode != 0:
        print(f"FaceFXWrapper returned error result when attempting to generate lip file for: {filename}")

def main():
    if len(sys.argv) > 1:
        esp_name = sys.argv[1]
    else:
        esp_name = ""
    
    if "ELEVENLABS_VOICEID" in os.environ and "ELEVENLABS_KEY" in os.environ:
        voice_id = os.getenv("ELEVENLABS_VOICEID") 
        api_key = os.getenv("ELEVENLABS_KEY")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            'xi-api-key': api_key,
            'Content-Type': 'application/json'
        }
    else:
        print("To use the elevenlabs API you must provide the voice_id and xi-api-key. Set the env variables ELEVENLABS_VOICEID and ELEVENLABS_KEY accordingly.")
        return
    
    output_folder = f"./generated"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    lines = parse_exported_dialogue_file("export.txt", esp_name)

    pbar = tqdm(lines, ascii=True)
    for filename, text in pbar:
        # Don't regenerated a voice file if it already exists
        if os.path.exists(f"{output_folder}/{filename}"):
            continue

        pbar.set_description(f"({filename}) Generating voice file")
        res = get_voice_file_for_line(url, headers, filename, text, output_folder)

        # If the API failed before we finished downloading everything, break.
        if res == False:
            break

        pbar.set_description(f"({filename}) Generating lip file")
        generate_lip_file(filename, text, output_folder)

main()
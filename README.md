# bsa-voice-ai-replacer
wip script to automate replacing mod voice dialogue with AI generated voice from Elevenlabs.

This script generates .wav files from an elevenlabs generated voice with the original file name so its incredibly easily to replace & overwrite.

In the CreationKit you can select a NPC's voice and "Export dialogue" which gives you a formatted text file with lots of information but most importantly the original voice .wav file name and the actual text to be spoken.

Unforunately repacking BSA's after extracting them is messy, and although the generated voice files are amazing, the lip files for the previous voice will most likely be off, and there doesn't seem to be any good way of programmatically generating lip files from .wav's. Using the CreationKit itself is an incredibly waste of time and slow.

Thankfully third party applications like FaceFXWrapper exist, which allows for CLI generation of lip files from a .wav. No library version for this functionality, but it will have to do.

So I leave this here for the future, currently the method I got working was this:
- Get exported dialogue file and run this script
- Use FaceFXWrapper to generate .lip files for all of the newly generated .wav files.
- BSArch to extract original mod's BSA
- YakitoriAudioConverter to convert our newly generated AI .wav & .lip files into .fuz
- replace original .fuz files with our new ones 
- BSArch to repack the BSA 
- Replace mod's original BSA with our new one with replaced audio. 

Will overtime try and automate each step through this script somehow, most likely as python subprocesses unfortunately.
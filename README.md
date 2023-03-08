# bsa-audio-ai-replacer
wip script to automate replacing mod dialogue with ai generated voice from elevenlabs.

This script generates .wav files from an elevenlabs generated voice with the original file name so its incredibly easily to replace & overwrite.


In the CreationKit you can select a NPC's voice and "Export dialogue" which gives you a formatted text file with lots of information but most importantly the original voice .wav file name and the actual text to be spoken.

Unforunately repacking BSA's after extracting them is messy, and although the generated voice files are amazing, the lip files for the previous voice will most likely be off, and there doesn't seem to be any good way of programmatically generating lip files from .wav's. Using the CreationKit itself is an incredibly waste of time and slow, and using third party tools like FaceFXWrapper didn't work for me.

So I leave this here for the future potentially, currently the method I got working (with out-of-sync lip files) was this:
- Get exported dialogue file and run this script
- BSArch to extract original mod's BSA
- YakitoriAudioConverter to unpack .fuz audio files from BSA into .xwm & .lip 
- YakitoriAudioConverter to convert our newly generated AI .wav files into .xwm 
- replace original .wxm files with new ones 
- YakitoriAudioConverter to convert .xwm & .lip back into .fuz  
- BSArch to repack the BSA 
- Replace mod's original BSA with our new one with replaced audio. 

This works, but the lip files are outdated. Let me know if you can think of a way to generate the lip files in this pipeline!

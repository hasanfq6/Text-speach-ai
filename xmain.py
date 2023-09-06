import argparse,subprocess,uuid,eyed3
from time import sleep
from elevenlabs import *

#TODO Adam: pNInz6obpgDQGcFmaJgB
#TODO Clyde: 2EiwWnXFnvU5JabPnv8n

# Function to read voice mappings from the voices.txt file
def read_voice_mappings(file_path):
    voice_mappings = {}
    try:
        with open(file_path, 'r') as voices_file:
            for line in voices_file:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    voice_name, voice_id = parts[0], parts[1]
                    voice_mappings[voice_name] = voice_id
    except FileNotFoundError:
        print("Voices file (voices.txt) not found.")
    return voice_mappings

# Define the path to the voices.txt file
voices_file_path = 'voices.txt'

# Read voice mappings from voices.txt
voice_id_mapping = read_voice_mappings(voices_file_path)

def generate_and_save_audio(text, voice, output_file):
    # Generate audio from the provided text with the specified voice
    audio = generate(text=text, voice=voice)

    # Save the audio to the specified output file
    with open(output_file, "wb") as audio_file:
        audio_file.write(audio)

def list_voices():
    print("Available voices:")
    for voice_name in voice_id_mapping:
        print(voice_name)

def main():
    parser = argparse.ArgumentParser(description="Generate and save audio from text or file")
    parser.add_argument("-t", "--text", help="Text to generate audio from")
    parser.add_argument("-o", "--output", help="Output audio file name")
    parser.add_argument("-f", "--file", help="File in txt form (task: one per line)")
    parser.add_argument("-l", "--line", default="1", help="Starting line number (default: 1)")
    parser.add_argument("-v", "--voice", default="Clyde", help="Name of the voice (default: 'Adam')")
    parser.add_argument("-s", "--stabel", type=float, default=0.75, help="Voice stability MAX:0.99(default: 0.75)")
    parser.add_argument("-b", "--boost", type=float, default=0.80, help="Voice stability boost MAX:0.99(default: 0.80)")
    parser.add_argument("--voices-list", action="store_true", help="List available voices in database")
    parser.add_argument("--cheat", action="store_true", help="display cheat to bypass limitaion restriction(only for legal)")
    parser.add_argument("--api-key", help="Set the API key")

    args = parser.parse_args()

    # Set the API key if provided
    if args.api_key:
        set_api_key(args.api_key)
        print(f"API key set: {args.api_key}")
        return
    if args.cheat:
        # Run cheat.py using subprocess
        subprocess.run(["python", "cheat.py"])
        return

    if args.voices_list:
        list_voices()
        return

    if args.file:
        with open(args.file, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if line_number < int(args.line):
                    continue  # Skip lines before the specified starting line

                input_text = line.strip()
                if not input_text:
                    print("Empty task, skipping.")
                    continue

                if args.voice:
                    if args.voice in voice_id_mapping:
                        voice_id = voice_id_mapping[args.voice]
                    else:
                        print(f"Voice '{args.voice}' not found in voices.txt. Using default voice ID.")
                        voice_id = "2EiwWnXFnvU5JabPnv8n"  # Set the default voice ID
                else:
                    print("No voice specified. Using default voice ID.")
                    voice_id = "2EiwWnXFnvU5JabPnv8n"  # Set the default voice ID

                selected_voice = Voice(
                    name=args.voice,
                    category='premade',
                    settings=VoiceSettings(stability=args.stabel, similarity_boost=args.boost),
                    voice_id=voice_id
                )

                print(f"Task ({line_number}): {input_text}")
                sleep(8)
                words = input_text.split()
                segments = [words[i:i + 37] for i in range(0, len(words), 37)]

                for segment_number, segment in enumerate(segments, start=1):
                    segment_text = " ".join(segment)
                    segment_output_file = f"segment_{line_number}_{segment_number}.wav"
                    generate_and_save_audio(segment_text, selected_voice, segment_output_file)

                combined_audio = b""
                for segment_number in range(1, len(segments) + 1):
                    segment_output_file = f"segment_{line_number}_{segment_number}.wav"
                    with open(segment_output_file, "rb") as segment_audio_file:
                        combined_audio += segment_audio_file.read()
                output_file = f"Audio/Motive_pri_{str(uuid.uuid4())[:8]}{line_number}.wav"
#                output_file = f"output_{line_number}.wav"
                with open(output_file, "wb") as combined_audio_file:
                    combined_audio_file.write(combined_audio)
                print(f"\n\033[32mTask completed (\033[36m{line_number}\033[32m)\033[0m: {input_text}\n")
                os.system(f"python 1sample.py --file {output_file} --image Audio/1.png")
    elif args.text and args.output:
        # ... (rest of your code)
            input_text = args.text
            output_file = args.output
        
            if args.voice:
                if args.voice in voice_id_mapping:
                    voice_id = voice_id_mapping[args.voice]
                else:
                    print(f"Voice '{args.voice}' not found in voices.txt. Using default voice ID.")
                    voice_id = "2EiwWnXFnvU5JabPnv8n"  # Set the default voice ID
            else:
                print("No voice specified. Using default voice ID.")
                voice_id = "2EiwWnXFnvU5JabPnv8n"  # Set the default voice ID
        
            selected_voice = Voice(
                name=args.voice,
                category='premade',
                settings=VoiceSettings(stability=args.stabel, similarity_boost=args.boost),
                voice_id=voice_id
            )
        
            print(f"{input_text}")
            sleep(8)
            words = input_text.split()
            segments = [words[i:i + 37] for i in range(0, len(words), 37)]
        
            for segment_number, segment in enumerate(segments, start=1):
                segment_text = " ".join(segment)
                segment_output_file = f"segment_{segment_number}.wav"
                generate_and_save_audio(segment_text, selected_voice, segment_output_file)
        
            combined_audio = b""
            for segment_number in range(1, len(segments) + 1):
                segment_output_file = f"segment_{segment_number}.wav"
                with open(segment_output_file, "rb") as segment_audio_file:
                    combined_audio += segment_audio_file.read()
        
            with open(output_file, "wb") as combined_audio_file:
                combined_audio_file.write(combined_audio)
            print(f"Combined audio saved as '{output_file}'")
            os.system(f"python 1sample.py --file {output_file} --image Audio/1.png")
    else:
        print("Please provide either --file or both --text and --output, -h.")

if __name__ == main():
  try:
    main()
  except KeyError:
    print("voice error")

import eyed3
import argparse

def set_audio_metadata(audio_file, title, artist, album, image_file):
    try:
        audio = eyed3.load(audio_file)
        if audio.tag is None:
            audio.initTag()
        
        audio.tag.title = title
        audio.tag.artist = artist
        audio.tag.album = album
        
        # Embed the image as cover art
        if image_file:
            with open(image_file, "rb") as image:
                audio.tag.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, image.read(), "image/jpeg")
        
        audio.tag.save()
        print("Metadata and image added successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set metadata and add an image to an audio file")
    parser.add_argument("--files", help="Path to the audio file")
    parser.add_argument("--title", help="Title of the audio")
    parser.add_argument("--artist", help="Artist of the audio")
    parser.add_argument("--album", help="Album name of the audio")
    parser.add_argument("--image", help="Path to the image file (cover art)")
    
    args = parser.parse_args()
    
    if args.files:
        audio_file = args.files
        title = args.title or "Nami's speech"
        artist = args.artist or "Hasanfq6"
        album = args.album or "Motivational speech"
        image_file = args.image
        
        set_audio_metadata(audio_file, title, artist, album, image_file)
    else:
        print("Please provide the path to the audio file using the --files argument.")

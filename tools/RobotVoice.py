import pyttsx3

def text_to_speech(text, voice_id=None, rate=None):
    try:
        engine = pyttsx3.init()
        
        # Debug: Print available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"Voice {i}: {voice.name}")

        # Changing voice
        if voice_id is not None:
            if voice_id < len(voices):
                engine.setProperty('voice', voices[voice_id].id)
                print(f"Set voice to: {voices[voice_id].name}")
            else:
                print("Invalid voice ID. Using default voice.")

        # Changing speed
        if rate:
            engine.setProperty('rate', rate)
            print(f"Set rate to: {rate}")

        # Debug: Print current properties
        print(f"Current voice: {engine.getProperty('voice')}")
        print(f"Current rate: {engine.getProperty('rate')}")

        print("Attempting to say:", text)
        engine.say(text)
        print("Running engine...")
        engine.runAndWait()
        print("Engine finished.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    text = "Hello, world! My name is AI"
    voice_id = 73  # Start with the first voice
    rate = 150  # Adjust this number for different speed rates
    text_to_speech(text, voice_id, rate)
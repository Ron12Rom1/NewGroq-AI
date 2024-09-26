import os
from groq import Groq
from dotenv import load_dotenv
import datetime as dat

now = dat.datetime.now()

# from tools.Recorder import record_audio
# from tools.VoiceReconizer import transcribe_audio
from tools.RobotVoice import text_to_speech

load_dotenv()

# Access the API key
API_KEY = os.getenv('API_KEY')

client = Groq(api_key=API_KEY)


with open("who-are-you.txt", "r") as f1:
    you_are = f1.read()


userIn = "Start with an opening line saying that you are ready"
while userIn != "exit()":

    with open ("memory.txt", "r+") as mem:
        memory = mem.read()

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": str(you_are) + "It is: " + str(dat.datetime.now()) + 
             ".   this is what you remember from our previos conversation: " + str(memory)},
            {"role": "user", "content": userIn}
        ],
        temperature=1.5,
        max_tokens=1084,
        top_p=1,
        stream=True,
        stop=None,
        frequency_penalty=2.0,
        # seed=99999999
    )

    print("\n")
    out = []
    with open("memory.txt", "a") as mem:
        for chunk in completion:
            out.append((chunk.choices[0].delta.content or ""))
            print(chunk.choices[0].delta.content or "", end="")
        text_to_speech(str("".join(out)), 1, 210)
        mem.write('user: ' + userIn + "\n")
        mem.write('you: ' + str("".join(out)) + "\n")
    
    try: userIn = input("\n:")
    except KeyboardInterrupt: exit()

with open("memory.txt", "r") as mem:
    with open("who-are-you.txt", "a") as whoAreYou:
        whoAreYou.write("\n\nPrivios conversetions:\n" + mem.read())
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Access the API key
API_KEY = os.getenv('API_KEY')

client = Groq(api_key=API_KEY)


with open("who-are-you.txt", "r") as f1:
    you_are = f1.read()


userIn = -1
while userIn != "exit()":

    with open ("memory.txt", "r+") as mem:
        memory = mem.read()

    userIn = input("\n:")

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": str(you_are) + ".   this is what you remember from our previos conversation: " + str(memory)},
            {"role": "user", "content": userIn}
        ],
        temperature=1.5,
        max_tokens=200,
        top_p=1,
        stream=True,
        stop=None,
        frequency_penalty=2.0,
    )

    print("\n")
    out = []
    with open("memory.txt", "a") as mem:
        for chunk in completion:
            out.append((chunk.choices[0].delta.content or ""))
            print(chunk.choices[0].delta.content or "", end="")
        mem.write('user: ' + userIn + "\n")
        mem.write('you: ' + str("".join(out)) + "\n")
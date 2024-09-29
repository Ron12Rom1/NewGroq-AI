import os
import requests
from groq import Groq
from dotenv import load_dotenv
import datetime as dat
import json

from tools.RobotVoice import text_to_speech

load_dotenv()

now = dat.datetime.now()

with open("filered-words.txt", "r") as f:
    filtered_words = f.read().splitlines()
print(filtered_words)

# Access the API key
API_KEY = os.getenv('API_KEY')

client = Groq(api_key=API_KEY)

def get_current_location():
    print("Called get_current_location")
    return "Beer Sheva, Israel"

def get_weather(location=None, unit="celsius"):
    print("Called get_weather")
    try:
        if location is None:
            location = get_current_location()
            if location is None:
                return "Sorry, I couldn't determine your current location."

        base_url = "https://api.open-meteo.com/v1/forecast"
        
        # First, get the coordinates for the location
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = requests.get(geocoding_url)
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if geo_data.get("results"):
                latitude = geo_data["results"][0]["latitude"]
                longitude = geo_data["results"][0]["longitude"]
            else:
                return f"Sorry, I couldn't find the location: {location}."
        else:
            return "Sorry, I couldn't retrieve the location coordinates."
        
        # Now get the weather data
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "temperature_unit": "fahrenheit" if unit.lower() == "fahrenheit" else "celsius"
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["current_weather"]["temperature"]
            wind_speed = data["current_weather"]["windspeed"]
            return f"The current weather in {location} is {temp}°{'F' if unit.lower() == 'fahrenheit' else 'C'} with a wind speed of {wind_speed} km/h."
        else:
            return f"Sorry, I couldn't retrieve the weather for {location}."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred while fetching the weather: {str(e)}"

with open("who-are-you.txt", "r") as f1:
    you_are = f1.read()

userIn = "Start with an opening line saying that you are ready"
while userIn != "exit()":

    with open ("memory.txt", "r+") as mem:
        memory = mem.read()

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and country, e.g. London, UK. If not provided, uses the current location."
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The unit of temperature to use. Defaults to celsius."
                            }
                        },
                        "required": []
                    }
                }
            }
        ],
        messages=[
            {"role": "system", "content": str(you_are) + "It is: " + str(dat.datetime.now()) + 
             ".   this is what you remember from our previous conversation: " + str(memory)},
            {"role": "user", "content": userIn}
        ],
        temperature=1.5,
        max_tokens=1084,
        top_p=1,
        stream=True,
        stop=None,
        frequency_penalty=2.0,
        tool_choice="auto",
    )

    print("\n")
    out = []
    with open("memory.txt", "a") as mem:
        for chunk in completion:
            if chunk.choices[0].delta.content:

                word = chunk.choices[0].delta.content
                new_word = chunk.choices[0].delta.content.strip()
                if new_word in filtered_words:
                    out.append(" FILTERED")
                else:
                    out.append(word)

            elif chunk.choices[0].delta.tool_calls:
                for tool_call in chunk.choices[0].delta.tool_calls:
                    if tool_call.function.name == "get_weather":
                        function_args = json.loads(tool_call.function.arguments)
                        weather_info = get_weather(**function_args)
                        out.append(weather_info)


        full_response = "".join(out)
        # print(out)
        # print(full_response)  # Print the response to console
        text_to_speech(full_response, 1, 210)
        mem.write('user: ' + userIn + "\n")
        mem.write('you: ' + full_response + "\n")
    
    try: 
        userIn = input("\n:")
    except KeyboardInterrupt: 
        break

with open("memory.txt", "r") as mem:
    with open("who-are-you.txt", "a") as whoAreYou:
        whoAreYou.write("\n\nPrevious conversations:\n" + mem.read())
        with open("memory.txt", "w") as memory:
            memory.write("")
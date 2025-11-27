import json
import re
import google.generativeai as genai
from .config import API_KEY, MODEL, SYSTEM_PROMPT

def extract_image_data(pil_image):
    #return default name and date
    if API_KEY == "":
        print("ERROR: API Key is missing in config.py")
        return {"date": "00-00-0000", "name": "Unknown"}
    
    #setup api
    genai.configure(api_key=API_KEY)

    try:
        #this is basically a class constructor
        model = genai.GenerativeModel(MODEL)

        #feed system prompt and image to model
        response = model.generate_content([SYSTEM_PROMPT, pil_image])

        #response is like an object, we only extract the text inside of it
        #response.text is like a json string, and now we remove any unecessary whtie space
        raw_text = response.text.strip()

        #clean the text in case of ai adds in extra stuff, just an extra safety
        #sometimes ai returns with ```json{...}``` or other text garbage
        #re.DOTALL means across all lines
        #re.search returns a "match" object
        #use nongreedy regex
        match = re.search(r'\{.*?\}', raw_text, re.DOTALL)

        #did we find {}? if so lets set "{...}"" to be raw_text
        if match:
            raw_text = match.group(0)
        else:
            print("Could not find any JSON in the AI output.")
            return {"date": "00-00-0000", "name": "Unknown"}
        
        #this converts to a python dictionary
        data = json.loads(raw_text)

        #return a map with the correct key labels
        #usually we just pass in one parameter with [] to access key data
        #use .get() to safetly access each key in data
        #if key is missing then return default, thats the second parameter
        return {
            "date" : data.get("date", "00-00-0000"),
            "name" : data.get("name", "Unknown")
        }

    except Exception as e:
        print(f"AI READING ERROR: {e}")
        # Return default
        return {"date": "00-00-0000", "name": "Unknown"}
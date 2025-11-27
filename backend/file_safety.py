import re
from pathlib import Path

def clean_text(text):
    #replace any of these unsafe characters if seen with an empty char
    clean_text = re.sub(r'[\/":?*<>|]' , '', text)
    return clean_text.strip()

def generate_path(folder_path, date, name, extension):
    #clean the strings
    clean_date = clean_text(date)
    clean_name = clean_text(name)
    suffix = "_Eye_Examination"

    #put together
    filefront = f"{clean_date}_{clean_name}{suffix}"
    filename = f"{filefront}{extension}"

    #we replace old path with this new path to rename file in our main logic
    full_path = folder_path / filename

    #check if filename already exists using .exists()
    #if so, we create a new filename and see if it exists
    #terminates once it is not found
    counter = 1
    while full_path.exists():
        new_filename = f"{filefront}_{counter}{extension}"
        full_path = folder_path / new_filename
        counter += 1
    
    return full_path
import os

folder_path = "C:/Users/Daniel/Documents/Python/file_renamer/testfiles"
original_filename = "Screenshot 2025-11-26 100110.png"

old_file = os.path.join(folder_path, original_filename)
new_file = os.path.join(folder_path, "outline.png")

try:
    os.rename(old_file, new_file)
    print(f"Renamed '{original_filename}' to 'outline.png'")
except FileNotFoundError:
    print(f"File '{original_filename}' not found.")
except FileExistsError:
    print(f"File {original_filename}' already exists.")
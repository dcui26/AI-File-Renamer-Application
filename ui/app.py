import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import threading
from PIL import Image

from backend.pdf_methods import convert_pdf_to_images
from backend.file_safety import generate_path
from backend.ai_reader import extract_image_data
from backend.config import SUPPORTED_EXTENSIONS

class fileRenamer():
    def __init__(self, root):
        self.root = root

        #setup app
        self.root.geometry("500x400")
        self.root.title("File Renaming Application")

        self.selected_folder = ctk.StringVar(value = "Select folder")

        #create flag
        self.is_running = False

        self.setupUI()


    def setupUI(self):
        self.root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.root.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.choose_file_button = ctk.CTkButton(
            self.root, 
            textvariable = self.selected_folder,
            fg_color = "#404040", 
            hover_color="#636363", 
            command=self.chooseFolder
        )
        self.choose_file_button.grid(row=7, column=2, columnspan=6, sticky="nsew", padx=10, pady=10)

        self.start_button = ctk.CTkButton(
            self.root, 
            text = "Start",
            command=self.pressStart
        )
        self.start_button.grid(row=8, column=3, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.stop_button = ctk.CTkButton(
            self.root, 
            text = "Stop",
            state="disabled", 
            command=self.pressStop
        )
        self.stop_button.grid(row=8, column=5, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.log_box = ctk.CTkTextbox(self.root, width=500, height=300, state="disabled")
        self.log_box.grid(row=1, column=1, rowspan=6, columnspan=8, sticky="nsew", padx=10, pady=10)


    def chooseFolder(self):
        folder = filedialog.askdirectory()
        #only update our stringvar if a folder is selected
        #critical for UX, if user cancels the display shouldn't change
        if folder:
            self.selected_folder.set(folder)

    def pressStart(self):
        folder_path = self.selected_folder.get()
        if folder_path == "Select folder" or folder_path == "":
            print("Please select a valid folder.")
            return
        
        #set flag = true
        self.is_running = True

        #turn off button once processing
        self.start_button.configure(state="disabled", text="Processing...")
        self.stop_button.configure(state="normal", text="Stop")
        #use daemon thread, if close program thread could still run unintentionally
        file_processor = threading.Thread(target=self.processFolder, daemon=True)
        file_processor.start()

    def processFolder(self):
        #setup path
        path_string = self.selected_folder.get()
        folder_path = Path(path_string)

        #create a folder to store processed files
        processed_files = folder_path / "processed"
        #make a folder, and check if it already exists
        #if so, continue, if not create folder
        processed_files.mkdir(exist_ok=True)

        #fill a list with everything in the directory
        files = list(folder_path.iterdir())
        total = len(files)

        self.logMessage("Processing...")

        #iterate over all files
        for i in range(total):
            #check flag
            if not self.is_running:
                self.logMessage("**Stopped by user**")
                break

            file_path = files[i]
            
            #double check all items are actually files
            #for ex, if its a folder, skip iteration
            if not file_path.is_file():
                continue
            
            #ensure that suffix of our filename is allowed
            #use .lower() for extra safety
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                #first initialize an image variable
                pil_image = None
                is_pdf = file_path.suffix.lower() == ".pdf"

                if is_pdf:
                    images = convert_pdf_to_images(file_path)
                    num_pages = len(images)
                    for j in range(num_pages):
                        original_img = images[j]

                        #crop image
                        width, height = original_img.size
                        cropped_img = original_img.crop((width // 2, 0, width, height // 4))

                        #check
                        #cropped_img.show()

                        #get our dictionary from ai_reader.py
                        data = extract_image_data(cropped_img)

                        #get our new path from file_safety.py
                        newpath = generate_path(
                            processed_files, 
                            data["date"], 
                            data["name"], 
                            ".jpg"
                        )
                        original_img.save(newpath, "JPEG", quality=95)
                        self.logMessage(f"Saved: {newpath.name}")
                else: #if not pdf
                    pil_image = Image.open(file_path)
                    if pil_image:
                        original_img = pil_image
                        width, height = original_img.size
                        cropped_img = original_img.crop((0, 0, width, height // 2))

                        data = extract_image_data(cropped_img)
                        pil_image.close()

                        newpath = generate_path(
                            processed_files,
                            data["date"],
                            data["name"],
                            file_path.suffix
                        )
                        #rename the existing file with new path
                        file_path.rename(newpath)
                        self.logMessage(f"Renamed: {newpath.name}")

            except Exception as e:
                self.logMessage(f"ERROR on {file_path.name}: {e}") #.name only takes the name of the file, not the entire path
                print(e) #print to console for debugging reasons

        #cleanup
        self.is_running = False
        self.start_button.configure(state="normal", text="Start")
        self.stop_button.configure(state="disabled", text = "Stop")
        self.logMessage("Task completed")
        print("Task completed")

    def pressStop(self):
        #set flag = false
        self.is_running = False
        self.stop_button.configure(state="disabled", text="Stopped")
        self.start_button.configure(state="normal", text="Start")

    def logMessage(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        print(message) #backup print to console
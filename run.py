import customtkinter as ctk
from ui.app import fileRenamer

if __name__ == "__main__":
    root = ctk.CTk()
    app = fileRenamer(root)
    root.mainloop()
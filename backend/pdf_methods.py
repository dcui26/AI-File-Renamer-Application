from pathlib import Path
from pdf2image import convert_from_path
from .config import POPPLER_BIN_PATH

#takes in the path to the pdf file
def convert_pdf_to_images(pdf_path):
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    poppler_str = str(POPPLER_BIN_PATH)

    try:
        #300 dpi for good res
        #convert_from_path converts pdf file into images
        #one PIL.image.image file per page
        images = convert_from_path(
            str(pdf_path), 
            poppler_path = poppler_str,
            dpi = 300
        )
        return images
    
    except Exception as e:
        print(f"CRITICAL ERROR in convert_pdf_to_images: {e}")
        
        # Debugging Helper
        if "poppler" in str(e).lower():
            print(f"DEBUG: Config points to: {poppler_str}")
            print("HINT: Is the 'poppler' folder inside your project directory?")
        return []
from pathlib import Path

API_KEY = ""
MODEL = "gemini-2.5-flash"

current_file_path = Path(__file__).resolve()  
project_root = current_file_path.parent.parent
POPPLER_BIN_PATH = project_root / "poppler" / "bin"

SUPPORTED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

SYSTEM_PROMPT = """
You are a data entry specialist for a veterinary lab. 
Extract metadata from the clinical result image.

INSTRUCTIONS:

1. Date: Find the "Date:" label. Convert to MM-DD-YYYY.
   - Zero-pad single digits (e.g. 4/4/2025 -> 04-04-2025).
   - If missing, return "00-00-0000".

2. Name: Find the "Name:" label (usually near the top). Transcribe exactly.
   - CRITICAL: Ignore "Examiner", "Doctor", or "Owner".
   - If missing, return "Unknown".

3. Output ONLY a raw JSON object with keys "date" and "name".
   - Do not include Markdown or conversational text.

### REQUIRED JSON STRUCTURE:
{
    "date": "MM-DD-YYYY",
    "name": "PatientName"
}
"""
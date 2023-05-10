# Install all the required Python libraries given in requirements.txt
# Use 'pip install -r requirements.txt'

import time
from ura_extract import extract_info

# Download and install pytesseract from https://github.com/UB-Mannheim/tesseract/wiki
# Copy the installation path and add \tesseract.exe at the end and replace the given path
# Default tesseract.exe path looks like this
tesseract_path = r'C:\Users\<username>\AppData\Local\Tesseract-OCR\tesseract.exe'

start = time.time()
# The function extract_info() takes two arguments, you can read about their descriptions and data types
# in annotations.py
data = extract_info(tesseract_path, '258807')

end = time.time()

runtime = (end-start) # runtime in seconds

print("Data:\n", data)
print("\nRuntime:", runtime, "s")
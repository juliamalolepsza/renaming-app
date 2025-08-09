import easyocr
from pdf2image import convert_from_path
import numpy as np
import re
import os
# pdf_path = "/Users/juliamalolepsza/Downloads/PL_S0DRVRY_VP_01.pdf"
# images = convert_from_path(pdf_path)
#list of PIL images representing each page of pdf

folder = "/Users/juliamalolepsza/Downloads/"
reader = easyocr.Reader(['pl', 'en'], gpu=False)
vin_lpn_map = {}

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(folder, file)
        images = convert_from_path(pdf_path)

        temp_lpn = None
        vin_found = None

        for page_num, image in enumerate(images):
            results = reader.readtext(np.array(image))
            all_text = " ".join([text for _, text, _ in results])

            vin_match = re.search(r'(?<=\sE\s)\b[A-Z0-9]{17}\b', all_text)
            lpn_match = re.search(r'(?<=\sA\s)[0-9A-Z]{1,3}[\s][0-9A-Z]{3,5}\b', all_text)

            if lpn_match:
                temp_lpn = lpn_match.group()

            if vin_match:
                vin = vin_match.group()
                vin_last4 = vin[-4:]
            
            vin_lpn_map[vin_last4] = temp_lpn
print(vin_lpn_map)

            
        


   

import easyocr
from pdf2image import convert_from_path
import numpy as np
import re
import os

folder = "/Users/juliamalolepsza/Downloads/"
reader = easyocr.Reader(['pl', 'en'], gpu=False)
vin_lpn_map = {}


for file in os.listdir(folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(folder, file)
        images = convert_from_path(pdf_path)

        temp_lpn = None
        vin_last4 = None

        for page_num, image in enumerate(images):
            results = reader.readtext(np.array(image))
            all_text = " ".join([text for _, text, _ in results])

            print("page number ", page_num)
            print(all_text)

        #     vin_match = re.search(r'\b([A-Z0-9]{12}[0-9]{5})(?:\([A-Z0-9]+\))?\b', all_text)
        #     lpn_match = re.search(r'(?<=\sA\s)[0-9A-Z]{1,3}[\s][0-9A-Z]{3,5}\b', all_text)

        #     if lpn_match:
        #         temp_lpn = lpn_match.group()

        #     if vin_match:
        #         vin_last4 = vin_match.group(1)[-4:]
                
        # if vin_last4:
        #     if (vin_last4 not in vin_lpn_map) or (vin_lpn_map[vin_last4] is None):
        #         vin_lpn_map[vin_last4] = temp_lpn



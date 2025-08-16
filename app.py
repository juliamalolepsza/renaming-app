import easyocr
from pdf2image import convert_from_path
import numpy as np
import re
import os

folder = "/Users/juliamalolepsza/Downloads/"
reader = easyocr.Reader(['pl', 'en'], gpu=False)
vin_lpn_map = {}

categories = {
    "vp" : ["RZECZPOSPOLITA POLSKA", "POZWOLENIE CZASOWE"],
    "ec" : ["CEMT-Nachweis", "ECMT"],
    "coc" : ["CO2"]
}

mapping = {
        "vp": "_VP_01",
        "ec": "_EC_02",
        "coc": "_COC_03"
    }

def categorize_document(text):
    for category, keywords in categories.items():
        for key in keywords:
            if key.lower() in text.lower():
                return category
    return "other"

def name_document(folder, path, category, vin):
    
    extension = mapping.get(category, "_UNKNOWN")
    new_name = f"PL_{vin}{extension}.pdf"
    new_path = os.path.join(folder, new_name)
    os.rename(path, new_path)
    return 



def final_rename(folder, vin_lpn_map):
    inc = 0
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            old_path = os.path.join(folder, file)
            vin_match = re.search(r'([0-9]{4})', file)
            vin = vin_match.group()
            extension_match = re.search(r'_(VP_01|EC_02|COC_03)', file)
            if extension_match:
                extension = extension_match.group()
            else:
                extension = "_UNKNOWN"
            if vin in vin_lpn_map and vin_lpn_map[vin] is not None:
                lpn = vin_lpn_map[vin]
            else:
                lpn = "none" + str(inc)
                inc += 1
            final_name = f"PL_{lpn}{extension}.pdf"
            final_path = os.path.join(folder, final_name)
            os.rename(old_path, final_path)

            


# ================= ocr ===================

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(folder, file)
        images = convert_from_path(pdf_path)

        temp_lpn = None
        vin_last4 = None

        for page_num, image in enumerate(images):
            results = reader.readtext(np.array(image))
            all_text = " ".join([text for _, text, _ in results])

            vin_match = re.search(r'\b([A-Z0-9]{12}[0-9]{5})(?:\([A-Z0-9]+\))?\b', all_text)
            lpn_match = re.search(r'(?<=\sA\s)[0-9A-Z]{1,3}[\s][0-9A-Z]{3,5}\b', all_text)

            if lpn_match:
                temp_lpn = lpn_match.group().replace(" ", "")

            if vin_match:
                vin_last4 = vin_match.group(1)[-4:]

            doc_category = categorize_document(all_text)
                
        if vin_last4:
            if (vin_last4 not in vin_lpn_map) or (vin_lpn_map[vin_last4] is None):
                vin_lpn_map[vin_last4] = temp_lpn

        name_document(folder, pdf_path, doc_category, vin_last4)

print(vin_lpn_map)

final_rename(folder, vin_lpn_map)


            
        


   

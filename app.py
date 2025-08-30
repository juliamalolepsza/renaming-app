import easyocr
from pdf2image import convert_from_path
import numpy as np
import re
import os
import cv2

# folder = "/Users/juliamalolepsza/Downloads/"
reader = easyocr.Reader(['pl', 'en'], gpu=False)
vin_lpn_map = {}

categories = {
    "soft" : ["POZWOLENIE" "CZASOWE", "CEL", "WYDANIA", "CZASOWEGO"],
    "vp" : ["WSPÓLNOTA", "EUROPEJSKA", "DOWÓD", "REJESTRACYJNY", "DR", "DRBAU", "BAT", "DRIBAT", "BAR", "BAU"],
    "ec" : ["CEMT-Nachweis", "CEMT", "ECMT"],
    "coc" : ["CO2", "CO", "mg/kWh", "THC"]
}

extensions = {
        "soft" : "_VP_01",
        "vp": "_VP_01",
        "ec": "_EC_02",
        "coc": "_COC_03"
    }

def categorize_document(text):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                return category
    return None

count = 0

def name_document(folder, path, category, vin):
    extension = extensions.get(category, "_UNKNOWN")
    base_name = f"PL_{vin}{extension}"
    new_name = f"{base_name}.pdf"
    new_path = os.path.join(folder, new_name)

    counter = 1
    while os.path.exists(new_path):
        new_name = f"{base_name}_{counter}.pdf"
        new_path = os.path.join(folder, new_name)
        counter += 1
    os.rename(path, new_path)
    return



def final_rename(folder, vin_lpn_map):
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            old_path = os.path.join(folder, file)
            vin_match = re.search(r'([0-9]{4})', file) 
            vin = vin_match.group() if vin_match else "x"
            extension_match = re.search(r'_(VP_01|EC_02|COC_03)', file)
            if extension_match:
                extension = extension_match.group()
            else:
                extension = "_UNKNOWN"
            if vin in vin_lpn_map and vin_lpn_map[vin] is not None:
                lpn = vin_lpn_map[vin]
            else:
                lpn = vin


            base_name = f"PL_{lpn}{extension}"
            final_name = f"{base_name}.pdf"
            final_path = os.path.join(folder, final_name)

            counter = 1
            while os.path.exists(final_path):
                final_name = f"{base_name}_{counter}.pdf"
                final_path = os.path.join(folder, final_name)
                counter += 1

            os.rename(old_path, final_path)


def read_image(image):
    results = reader.readtext(np.array(image))
    all_text = " ".join([text for _, text, _ in results])
    return all_text    


def check_for_vp(image):
    image = np.array(image)
    qr_detector = cv2.QRCodeDetector()

    retval, points = qr_detector.detect(image)
    print(points)

    if points is None:
        return image, False
    
    cx = int(points[:,0,0].mean())
    cy = int(points[:,0,1].mean())
    (h, w) = image.shape[:2]

    if cx < w/2 and cy < h/2:
        image = cv2.rotate(image, cv2.ROTATE_180)    # top-left -> bottom-right
    elif cx > w/2 and cy < h/2:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) # top-right -> bottom-right
    elif cx < w/2 and cy > h/2:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE) # bottom-left -> bottom-right

    return image, True


# ================= ocr ===================

qr_detector = cv2.QRCodeDetector()

def process_images(folder):
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder, file)
            images = convert_from_path(pdf_path)

            temp_lpn = None
            vin_last4 = None

            for page_num, image in enumerate(images):

                image, has_qr = check_for_vp(image) #check if has qr -> then its vp - rotate

                all_text = read_image(image) 

                if has_qr:
                    doc_category = "vp"
                else:
                    doc_category = categorize_document(all_text)
                
                vin_match = re.search(r'\b([A-Z0-9]{12}[0-9]{5})(?:\([A-Z0-9]+\))?\b', all_text)
                lpn_match = re.search(r'\b[A-Z]{1}[A-Z0-9]{1,2}\s?[0-9A-Z]{4,5}\b', all_text)

                if lpn_match:
                    temp_lpn = lpn_match.group().replace(" ", "")

                if vin_match:
                    vin_last4 = vin_match.group(1)[-4:]

                if doc_category:
                    break
                    
            if vin_last4:
                if (vin_last4 not in vin_lpn_map) or (vin_lpn_map[vin_last4] is None):
                    vin_lpn_map[vin_last4] = temp_lpn

            name_document(folder, pdf_path, doc_category, vin_last4)


folder = "/Users/juliamalolepsza/Downloads/"
process_images(folder)

print(vin_lpn_map)

final_rename(folder, vin_lpn_map)


            
        


   

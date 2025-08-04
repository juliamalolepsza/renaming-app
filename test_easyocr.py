import easyocr
from pdf2image import convert_from_path
import numpy as np
import re

pdf_path = "/Users/juliamalolepsza/Downloads/PL_BAU51416_COC_03.pdf"
images = convert_from_path(pdf_path)

reader = easyocr.Reader(['pl'], gpu=False)

for page_num, image in enumerate(images):
    print(f"\n--- Page {page_num + 1} ---")
    results = reader.readtext(np.array(image))

    if not results:
        print("No text found on this page.")
    else:
        for _, text, _ in results:
            print(text)



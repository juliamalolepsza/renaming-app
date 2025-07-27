import sys, pymupdf

dir_in = "C:\Users\Julia\Downloads"

def load_pdfs():
    return []

def convert_all_pdf():
    all_pdfs_images = []
    for pdf_fileName in load_pdfs:
        all_pdfs_images.append(convert_pdf_to_image(pdf_fileName))


def convert_pdf_to_image(pdfName):
    images = []
    doc = pymupdf.open(pdfName)
    for page in doc:
        pix = page.get_pixmap()


        return images

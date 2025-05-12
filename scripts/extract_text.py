import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from tqdm import tqdm

RAW_PDF_DIR = "../data/raw_pdfs"
TEXT_OUTPUT_DIR = "../data/processed_text"
OCR_IMAGE_DIR = "../data/ocr_images"

os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)
os.makedirs(OCR_IMAGE_DIR, exist_ok=True)

def extract_text_pdfplumber(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        print(f"pdfplumber failed for {pdf_path}: {e}")
        return None

def extract_text_ocr(pdf_path, pdf_name):
    try:
        images = convert_from_path(pdf_path)
        text_pages = []
        for i, img in enumerate(images):
            img_path = os.path.join(OCR_IMAGE_DIR, f"{pdf_name}_page_{i+1}.png")
            img.save(img_path, "PNG")
            text_pages.append(pytesseract.image_to_string(img))
        return "\n".join(text_pages)
    except Exception as e:
        print(f"OCR failed for {pdf_path}: {e}")
        return ""

def save_text(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    pdf_files = list(Path(RAW_PDF_DIR).glob("*.pdf"))

    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        filename = pdf_path.stem
        out_path = os.path.join(TEXT_OUTPUT_DIR, f"{filename}.txt")

        text = extract_text_pdfplumber(pdf_path)
        if not text or text.strip() == "":
            text = extract_text_ocr(pdf_path, filename)

        save_text(text, out_path)

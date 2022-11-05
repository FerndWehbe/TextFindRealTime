from pytesseract import image_to_string
import pytesseract


class Processor:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    def find_text(self, image):
        text: str = image_to_string(image)
        print(text)
        return text

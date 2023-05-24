import pytesseract
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
from pytesseract import TesseractError

from odbc import write_log


async def enhance_and_ocr(image, index):
    enhancer = ImageEnhance.Contrast(image)
    enhance_value = 1.5
    enhanced_image = enhancer.enhance(enhance_value)
    enhanced_image.save(f'enhanced_image_{index}.jpg')
    try:
        text = pytesseract.image_to_string(enhanced_image)
    except TesseractError as e:
        print("Error in OCR: ", e)
        write_log('OCR','Error in OCR',e)
        text = "No se puede leer el texto. Por favor, toma nuevamente la foto o mejora la imagen."
    if not text:
        return "No se puede leer el texto. Por favor, toma nuevamente la foto o mejora la imagen."
    return text

async def perform_ocr(image_path, is_pdf=False):
    texts = []
    try:
        if is_pdf:
            images = convert_from_path(image_path)
            for i, image in enumerate(images):
                text = await enhance_and_ocr(image, i)
                texts.append(text)
        else:
            image = Image.open(image_path)
            text = await enhance_and_ocr(image, 0)
            texts.append(text)

    except IOError:
        write_log('IOError','perform_ocr',"can't find file or read data")
        print("Error: can't find file or read data")
    if not texts:
        return "No se puede leer el texto. Por favor, toma nuevamente la foto o mejora la imagen."
    else:
        joined_text = '\n'.join(texts)
        return joined_text


# Print the text
#print(f'texto: {text}')
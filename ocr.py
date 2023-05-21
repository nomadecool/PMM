import pytesseract
from PIL import Image, ImageEnhance

async def perform_ocr(image_path):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(200)
    text = pytesseract.image_to_string(enhanced_image)
    return text

# Print the text
#print(f'texto: {text}')
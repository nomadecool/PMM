import pytesseract
from PIL import Image, ImageEnhance

async def perform_ocr(image_path):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    enhance_value = 1.5
    enhanced_image = enhancer.enhance(enhance_value)
    enhanced_image.save(f'enhanced_image{enhance_value}.jpg')
    text = pytesseract.image_to_string(enhanced_image)
    return text

# Print the text
#print(f'texto: {text}')
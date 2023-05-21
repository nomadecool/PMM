import pytesseract
from PIL import Image, ImageEnhance

# Get the path to the image
image_path = 'file_name.jpg'

# Read the image
image = Image.open(image_path)

# Create a contrast enhancer
enhancer = ImageEnhance.Contrast(image)

# Increase the contrast by 200%
enhanced_image = enhancer.enhance(200)

# Convert the image to text
text = pytesseract.image_to_string(enhanced_image)

# Print the text
print(f'texto: {text}')
from PIL import Image
import io

MAX_SIZE_BYTES = 1024 * 1024 * 5

def process_image(image_file):
    image_data = image_file.read()
    
    if len(image_data) <= MAX_SIZE_BYTES:
        return image_data, image_file.content_type
    
    img = Image.open(io.BytesIO(image_data))
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    width, height = img.size
    quality = 95
    
    while True:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=quality)
        compressed_data = img_byte_arr.getvalue()
        
        if len(compressed_data) <= MAX_SIZE_BYTES:
            break
        
        if quality > 30:
            quality -= 5
        else:
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), Image.LANCZOS)
    
    return compressed_data, 'image/jpeg'
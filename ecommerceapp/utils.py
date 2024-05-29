# ecommerceapp/utils.py

from rembg import remove
from PIL import Image, ImageDraw
from colorthief import ColorThief
import webcolors
import os
from io import BytesIO
import openai

def closest_color(rgb_tuple):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_tuple[0]) ** 2
        gd = (g_c - rgb_tuple[1]) ** 2
        bd = (b_c - rgb_tuple[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def create_grey_gradient(size):
    start_color = (200, 200, 200)
    end_color = (255, 255, 255)
    return create_gradient(size, start_color, end_color)

def create_yellow_gradient(size):
    start_color = (255, 255, 224)
    end_color = (255, 255, 192)
    return create_gradient(size, start_color, end_color)

def create_light_color_gradient(size):
    start_color = (173, 216, 230)
    end_color = (224, 255, 255)
    return create_gradient(size, start_color, end_color)

def create_gradient(size, start_color, end_color, direction='vertical'):
    base = Image.new('RGB', size, start_color)
    top = Image.new('RGB', size, end_color)
    mask = Image.new('L', size)
    mask_data = []
    for y in range(size[1]):
        for x in range(size[0]):
            if direction == 'vertical':
                mask_data.append(int(255 * (y / size[1])))
            elif direction == 'horizontal':
                mask_data.append(int(255 * (x / size[0])))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def center_foreground(background, foreground):
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size
    offset = ((bg_width - fg_width) // 2, (bg_height - fg_height) // 2)
    background.paste(foreground, offset, foreground)
    return background

def process_image(image):
    custom_size = (428, 570)
    
    img = Image.open(image)
    resized_img = img.resize(custom_size)

    # Remove background
    img_byte_arr = BytesIO()
    resized_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    R = remove(img_byte_arr)
    foreground = Image.open(BytesIO(R))

    ct = ColorThief(BytesIO(R))
    dominant_color = ct.get_color(quality=1)
    closest_named_color = closest_color(dominant_color)

    gradients = {
        'grey': create_grey_gradient(custom_size),
        'yellow': create_yellow_gradient(custom_size),
        'light': create_light_color_gradient(custom_size)
    }

    processed_images = []
    output_dir = 'media/output/'
    os.makedirs(output_dir, exist_ok=True)

    for color_name, gradient_background in gradients.items():
        final_image = center_foreground(gradient_background, foreground)
        output_filename = f'final_image_{color_name}.png'
        output_path = os.path.join(output_dir, output_filename)
        final_image.save(output_path)
        processed_images.append({
            'filename': output_filename,
            'url': f'/media/output/{output_filename}'
        })

    return processed_images, dominant_color, closest_named_color

def get_file_name(file_path):
    """
    Extracts the file name from the given file path.
    
    Args:
        file_path (str): The path of the file.
        
    Returns:
        str: The file name.
    """
    return os.path.basename(file_path)

import openai

openai.api_key = "ADD KEY HERE"

def chat_with_gpt(message):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=message,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=1.0
    )
    return response.choices[0].text.strip()

def process_message(message):
    return chat_with_gpt(message)
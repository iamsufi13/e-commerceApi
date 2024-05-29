# # ecommerceapp/views.py

# from django.shortcuts import render
# from django.conf import settings
# from .forms import ImageUploadForm
# from .utils import process_image, get_file_name
# import os
# from django.http import JsonResponse

# from PIL import Image as PILImage
# import openai

# def upload_image(request):
#     if request.method == 'POST' and request.FILES['image']:
#         image = request.FILES['image']
#         processed_images, dominant_color, closest_color_name = process_image(image)

#         return render(request, 'ecommerceapp/index.html', {
#             'processed_images': processed_images,
#             'dominant_color': dominant_color,
#             'closest_color_name': closest_color_name
#         })

#     return render(request, 'ecommerceapp/index.html')


# def generate_thumbnail_url(file_name, file_path):
#     thumbnail_name = f"thumbnail_{file_name}"
#     thumbnail_path = os.path.join(file_path, thumbnail_name)
    
#     if not os.path.exists(thumbnail_path):
#         image = PILImage.open(os.path.join(file_path, file_name))
#         image.thumbnail((300, 300))
#         image.save(thumbnail_path)
    
#     return os.path.join(settings.MEDIA_URL, 'output', thumbnail_name)


# def chat_with_gpt(message):
#     response = openai.Completion.create(
#             engine="gpt-3.5-turbo-instruct",
#             prompt=message,
#             max_tokens=300,
#             n=1,
#             stop=None,
#             temperature=1.0
#     )
#     return response.choices[0].text.strip()

# def chat_view(request):
#     if request.method == 'POST':
#         cloth_type = request.POST.get('cloth_type')
#         cloth_color = request.POST.get('cloth_color')

#         prompt = f"You: give a 4-5 line description for {cloth_type} of {cloth_color} Color  "
#         response = chat_with_gpt(prompt)

#         return render(request, 'ecommerceapp/chat_result.html', {'response': response})

#     return render(request, 'ecommerceapp/chat.html')

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import process_image, closest_color, get_file_name
import os
from PIL import Image as PILImage
import openai
from colorthief import ColorThief

openai.api_key = 'Api Key Here'

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

@api_view(['POST'])
def upload_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.FILES['image']
    processed_images, dominant_color, closest_color_name = process_image(image)
    
    return Response({
        'processed_images': processed_images,
        'dominant_color': dominant_color,
        'closest_color_name': closest_color_name
    })

@api_view(['POST'])
def process_chat(request):
    cloth_type = request.data.get('cloth_type')
    cloth_color = request.data.get('cloth_color')
    if not cloth_type or not cloth_color:
        return Response({'error': 'cloth_type and cloth_color are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    prompt = f"You: give a 4-5 line description for {cloth_type} of {cloth_color} Color"
    response = chat_with_gpt(prompt)
    
    return Response({'response': response})

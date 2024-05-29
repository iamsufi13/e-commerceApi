from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('api/upload-image/', views.upload_image, name='upload_image'),
    path('api/process-chat/', views.process_chat, name='process_chat'),
]
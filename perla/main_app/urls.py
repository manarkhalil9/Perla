from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('about/', views.about, name='about' ),
    path('visions/<int:vision_id>/', views.vision_detail, name='vision_detail'),
]

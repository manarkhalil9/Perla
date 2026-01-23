from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('visions/', views.vision_index, name='index'),
    path('visions/<int:vision_id>/', views.vision_detail, name='vision_detail'),
    path('visions/create/', views.VisionCreate.as_view(), name='vision_create'),
    path('visions/<int:pk>/update/', views.VisionUpdate.as_view(), name='vision_update'),
    path('visions/<int:pk>/delete/', views.VisionDelete.as_view(), name='vision_delete'),

    path('visions/<int:vision_id>/tasks/new/', views.task_create, name='task_create'),

]


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    # click vision
    path('select_vision/<int:vision_id>/', views.home, name='select_vision'),

    path('about/', views.about, name='about'),

    # full CRUD vision URLs
    path('visions/', views.vision_index, name='index'),
    path('visions/<int:vision_id>/', views.vision_detail, name='vision_detail'),
    path('visions/create/', views.VisionCreate.as_view(), name='vision_create'),
    path('visions/<int:pk>/update/', views.VisionUpdate.as_view(), name='vision_update'),
    path('visions/<int:pk>/delete/', views.VisionDelete.as_view(), name='vision_delete'),

    # full CRUD visiontask URLs
    path('visions/<int:vision_id>/add_task/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.VisionTaskUpdate.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.VisionTaskDelete.as_view(), name='task_delete'),

    # todo URLs
    path('todos/add/', views.todo_add_form, name='todo_add_form'),
    path('todos/<int:todo_id>/toggle/', views.todo_toggle, name='todo_toggle'),
    path('todos/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
    path('todos/<int:todo_id>/edit/', views.todo_edit, name='todo_edit'),


    # URL to handle adding a VisionTask to the To-Do list
    path('tasks/<int:task_id>/to-todo/', views.todo_from_task, name='todo_from_task'),


    path('accounts/signup/', views.signup, name='signup'),

]

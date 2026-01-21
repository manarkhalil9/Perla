from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Vision

# Create your views here.
def home(request):
    visions = Vision.objects.all()
    return render(request, 'visions/index.html', {'visions': visions})

def vision_detail(request, vision_id):
    vision = Vision.objects.get(id=vision_id)
    return render(request, 'visions/detail.html', {'vision': vision})

def about(request):
    return render(request, 'about.html')
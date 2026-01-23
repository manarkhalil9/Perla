from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Vision, VisionTask
from .forms import VisionTaskForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def vision_index(request):
    visions = Vision.objects.all()
    return render(request, 'visions/index.html', {'visions': visions})

def vision_detail(request, vision_id):
    vision = Vision.objects.get(id=vision_id)
    task_form = VisionTaskForm()
    return render(request, 'visions/detail.html', {'vision': vision, 'task_form': task_form})

class VisionCreate(CreateView):
    model = Vision
    fields = ['name', 'description', 'target_month', 'image']
    success_url = '/visions/'

    # def form_valid(self, form):
    #    form.instance.user = self.request.user
    #    return super().form_valid(form)

class VisionUpdate(UpdateView):
    model = Vision
    fields = ['name', 'description', 'target_month', 'image']

class VisionDelete(DeleteView):
    model = Vision
    success_url = '/visions/'

def task_create(request, vision_id):
    vision = Vision.objects.get(id=vision_id)

    if request.method == 'POST':
        form = VisionTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.vision = vision
            task.save()
            return redirect('vision_detail', vision_id)

    else:
        form = VisionTaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'vision': vision
    })


from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Vision, VisionTask, TodoItem
from .forms import VisionTaskForm

# Create your views here.

# home
def home(request):
    todos = TodoItem.objects.all()
    return render(request, 'home.html', {'todos': todos})

# about
def about(request):
    return render(request, 'about.html')

# visions
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

# update vision
class VisionUpdate(UpdateView):
    model = Vision
    fields = ['name', 'description', 'target_month', 'image']

# delete vision
class VisionDelete(DeleteView):
    model = Vision
    success_url = '/visions/'

# vision tasks
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

    return render(request, 'main_app/task_form.html', {'form': form, 'vision': vision})

# update vision task
class VisionTaskUpdate(UpdateView):
    model = VisionTask
    fields = ['title', 'month']

# delete vision task
class VisionTaskDelete(DeleteView):
    model = VisionTask
    success_url = '/visions/'

# todo list
def todo_add(request):
    if request.method == 'POST':
        TodoItem.objects.create(
            title=request.POST['title'],
            date=request.POST['date'],
            priority=request.POST['priority']
        )
        return redirect('home')
    
# change status
def todo_toggle(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect('home')

# delete 
def todo_delete(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.delete()
    return redirect('home')


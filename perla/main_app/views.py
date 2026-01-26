from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Vision, VisionTask, TodoItem
from .forms import VisionTaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .utils import get_quote

# Create your views here.

# home
@login_required
def home(request):
    todos = TodoItem.objects.filter(user=request.user)
    visions = Vision.objects.filter(user=request.user)
    quote_data = get_quote
    return render(request, 'home.html', {'todos': todos, 'quote':quote_data, 'visions':visions})

# about
def about(request):
    return render(request, 'about.html')

# visions
@login_required
def vision_index(request):
    visions = Vision.objects.all()
    return render(request, 'visions/index.html', {'visions': visions})

@login_required
def vision_detail(request, vision_id):
    vision = Vision.objects.get(id=vision_id)
    task_form = VisionTaskForm()
    return render(request, 'visions/detail.html', {'vision': vision, 'task_form': task_form})

class VisionCreate(LoginRequiredMixin, CreateView):
    model = Vision
    fields = ['name', 'description', 'target_month', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# update vision
class VisionUpdate(LoginRequiredMixin, UpdateView):
    model = Vision
    fields = ['name', 'description', 'target_month', 'image']

# delete vision
class VisionDelete(LoginRequiredMixin, DeleteView):
    model = Vision
    success_url = '/visions/'

# vision tasks
@login_required
def task_create(request, vision_id):
    vision = Vision.objects.get(id=vision_id)

    if request.method == 'POST':
        form = VisionTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.vision = vision
            new_task.user = request.user
            new_task.save()
            return redirect('vision_detail', vision_id=vision_id)
    else:
        form = VisionTaskForm()

    return render(request, 'main_app/task_form.html', {'form': form, 'vision': vision})


# update vision task
class VisionTaskUpdate(LoginRequiredMixin, UpdateView):
    model = VisionTask
    fields = ['title', 'month']

# delete vision task
class VisionTaskDelete(LoginRequiredMixin, DeleteView):
    model = VisionTask
    success_url = '/visions/'

# todo list
@login_required
def todo_add(request):
    if request.method == 'POST':
        TodoItem.objects.create(
            title=request.POST['title'],
            date=request.POST['date'],
            priority=request.POST['priority'],
            user=request.user
        )
        return redirect('home')
    
# change status
@login_required
def todo_toggle(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect('home')

# delete 
@login_required
def todo_delete(request, todo_id):
    todo = TodoItem.objects.get(id=todo_id)
    todo.delete()
    return redirect('home')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid signup - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

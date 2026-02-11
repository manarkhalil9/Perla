from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Vision, VisionTask, TodoItem
from .forms import VisionTaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .utils import get_quote
from datetime import date

# Create your views here.

# home
@login_required
def home(request, vision_id=None):

    # get todays date
    today = date.today()

    # chack session for sorted quote
    sorted_date = request.session.get('quote_date')
    sorted_quote = request.session.get('daily_quote')

    # if there is no save date yet or the saved date is not today
    if sorted_date != str(today):
        # if new day generate new quote
        # generate new random quote
        quote_data = get_quote()
        # save new quote, and todays date inside the session, so it wont changed again today
        request.session['daily_quote'] = quote_data
        request.session['quote_date'] = str(today)
    else:
        # if same day reuse sorted quote
        quote_data = sorted_quote

    todos = TodoItem.objects.filter(user=request.user)

    active_todos = todos.filter(is_done=False).order_by('date')
    completed_todos = todos.filter(is_done=True).order_by('-date')

    visions = Vision.objects.filter(user=request.user).prefetch_related('visiontask_set')

    selected_vision = None
    timeline = []

    # if user clicks a vision
    if vision_id:
        # Get the selected vision
        selected_vision = Vision.objects.get(id=vision_id, user=request.user)

        month_order = [
            'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
        ]

        # get all tasks of this vision
        tasks = VisionTask.objects.filter(vision=selected_vision, user=request.user)

        # if no tasks => nothing to show
        if tasks.exists():
            # find earliest month that has tasks
            task_month_indexes = [month_order.index(t.month) for t in tasks]
            start_index = min(task_month_indexes)

            # stop at target month
            end_index = month_order.index(selected_vision.target_month)

            months_to_show = month_order[start_index:end_index + 1]

            # filter the tasks related to this month
            for month in months_to_show:
                month_tasks = tasks.filter(month=month)

                # add is_added flag to each task
                for task in month_tasks:
                    task.is_added = TodoItem.objects.filter(task=task, user=request.user).exists()

                total = month_tasks.count()
                # count done tasks
                done = month_tasks.filter(todoitem__is_done=True, todoitem__user=request.user).distinct().count()

                # check if at least one task is added to todo but not done
                added_not_done = month_tasks.filter(todoitem__is_done=False, todoitem__user=request.user).distinct().exists()
                # decide status
                if total > 0 and done == total:
                    status = 'done'
                elif added_not_done:
                    status = 'progress'
                elif total > 0:
                    status = 'planned'
                else:
                    status = 'empty'

                timeline.append({
                    'month': month,
                    'tasks': month_tasks,
                    'status': status,
                    'circle_status': status,
                })

    return render(request, 'home.html', {
        'active_todos': active_todos,
        'completed_todos': completed_todos,
        'quote': quote_data,
        'visions': visions, 
        'selected_vision': selected_vision,
        'timeline': timeline,
    })

# about
def about(request):
    return render(request, 'about.html')

# visions
@login_required
def vision_index(request):
    month_order = [
        'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
        'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
    ]

    visions = Vision.objects.filter(user=request.user)

    # custom sort by month order
    visions = sorted(visions, key=lambda v: month_order.index(v.target_month))
    
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
    template_name = 'main_app/vision_form.html'

    def form_valid(self, form):
        # Save the form first
        self.object = form.save()
        # Redirect to the vision detail page using redirect
        return redirect('vision_detail', vision_id=self.object.id)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vision'] = self.object.vision  # pass the related vision
        return context

    def form_valid(self, form):
        # Save the task first
        self.object = form.save()
        # Redirect to the related vision detail page
        return redirect('vision_detail', vision_id=self.object.vision.id)

# delete vision task
class VisionTaskDelete(LoginRequiredMixin, DeleteView):
    model = VisionTask
    success_url = '/visions/'

# todo list
@login_required
def todo_add_form(request):
    if request.method == 'POST':
        is_important = 'is_important' in request.POST

        TodoItem.objects.create(
            title=request.POST['title'],
            date=request.POST['date'],
            priority='high' if is_important else 'low',
            user=request.user
        )
        return redirect('home')
    return render(request, 'main_app/addTodo.html')
    
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

# edit
@login_required
def todo_edit(request, todo_id):
    # get todo that belongs to current user only
    todo = TodoItem.objects.get(id=todo_id, user=request.user)

    if request.method == 'POST':
        is_important = 'is_important' in request.POST
        # update fields from form 
        todo.title = request.POST['title']
        todo.date = request.POST['date']
        todo.priority='high' if is_important else 'low',
        todo.save()

        return redirect('home')
    return render(request, 'main_app/editTodo.html', {'todo': todo})

# add a todo from a vision task (+ button in timeline)
@login_required
def todo_from_task(request, task_id):
    # ensure the user owns the task
    task = VisionTask.objects.get(id=task_id, user=request.user)

    # Only create if it doesn't exist yet
    if not TodoItem.objects.filter(task=task, user=request.user).exists():
        TodoItem.objects.create(
            title=task.title,
            priority='medium',
            # required field, use today
            date=date.today(),  
            user=request.user,
            task=task,
        )
    return redirect('select_vision', vision_id=task.vision.id)

# auth
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

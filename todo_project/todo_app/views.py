from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task
from .forms import TaskForm

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Mark task complete/incomplete
    if request.method == 'POST' and 'toggle_task' in request.POST:
        task_id = request.POST.get('toggle_task')
        task = Task.objects.filter(id=task_id, user=request.user).first()
        if task:
            task.complete = not task.complete
            task.save()
        return redirect('home')

    # Delete task
    if request.method == 'POST' and 'delete_task' in request.POST:
        task_id = request.POST.get('delete_task')
        Task.objects.filter(id=task_id, user=request.user).delete()
        return redirect('home')

    # Add task
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    if request.method == 'POST' and 'delete_task' not in request.POST and 'toggle_task' not in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home')

    return render(request, 'todo_app/home.html', {'tasks': tasks, 'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'todo_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'todo_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

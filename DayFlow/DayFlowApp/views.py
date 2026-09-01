from datetime import date as date_cls

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, TaskForm
from .models import Task, TaskCompletion

WEEKDAYS_RU = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно 🎉')
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'DayFlowApp/register.html', {'form': form})


@login_required
def task_list(request):
    """Задачи на сегодня — главная страница."""
    today = date_cls.today()
    weekday = today.weekday()

    all_active = Task.objects.filter(user=request.user, is_active=True)
    todays_tasks = [t for t in all_active if t.occurs_on(today)]
    todays_tasks.sort(key=lambda t: t.time)

    completed_ids = set(
        TaskCompletion.objects.filter(
            task__in=todays_tasks, date=today, completed=True
        ).values_list('task_id', flat=True)
    )

    return render(request, 'DayFlowApp/task_list.html', {
        'tasks': todays_tasks,
        'completed_ids': completed_ids,
        'today': today,
        'weekday_name': WEEKDAYS_RU[weekday],
        'done_count': len(completed_ids),
        'total_count': len(todays_tasks),
    })


@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    today = date_cls.today()
    completion, created = TaskCompletion.objects.get_or_create(
        task=task, date=today, defaults={'completed': True}
    )
    if not created:
        completion.completed = not completion.completed
        completion.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def all_tasks(request):
    """Список всех задач пользователя для управления."""
    tasks = Task.objects.filter(user=request.user).order_by('-is_recurring', 'time')
    return render(request, 'DayFlowApp/all_tasks.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Задача «{task.title}» создана!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'DayFlowApp/task_form.html', {
        'form': form, 'heading': 'Новая задача', 'is_edit': False
    })


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Задача «{task.title}» обновлена!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'DayFlowApp/task_form.html', {
        'form': form, 'heading': 'Редактировать задачу', 'is_edit': True
    })


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Задача «{title}» удалена.')
        return redirect('all_tasks')
    return render(request, 'DayFlowApp/task_confirm_delete.html', {'task': task})

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', {'exception': str(exception)}, status=404)
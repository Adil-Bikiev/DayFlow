from datetime import date as date_cls
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegisterForm, TaskForm
from .models import Task, TaskCompletion

WEEKDAYS_RU = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ждём подтверждения почты
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            confirm_url = request.build_absolute_uri(
                reverse('confirm_email', args=[uid, token])
            )

            message = render_to_string('DayFlowApp/email/confirm_email.txt', {
                'user': user,
                'confirm_url': confirm_url,
            })
            send_mail(
                subject='Подтверди свою почту — DayFlow',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return redirect(f"{reverse('check_email')}?email={quote(user.email)}")
    else:
        form = RegisterForm()
    return render(request, 'DayFlowApp/register.html', {'form': form})


def check_email_view(request):
    email = request.GET.get('email', '')
    return render(request, 'DayFlowApp/check_email.html', {'email': email})


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Почта подтверждена! Добро пожаловать в DayFlow 🎉')
        return redirect('task_list')

    messages.error(request, 'Ссылка подтверждения недействительна или устарела.')
    return redirect('login')


@login_required
def task_list(request):
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
    return render(request, '404.html', status=404)
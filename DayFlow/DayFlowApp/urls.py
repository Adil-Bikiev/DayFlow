from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', views.toggle_complete, name='toggle_complete'),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='DayFlowApp/login.html',
            redirect_authenticated_user=True,   # <-- ключевая правка
        ),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register, name='register'),
]
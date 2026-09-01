from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, WEEKDAYS


class TaskForm(forms.ModelForm):
    repeat_days = forms.MultipleChoiceField(
        choices=[(str(k), v) for k, v in WEEKDAYS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Повторять по дням',
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'time', 'is_recurring', 'repeat_days', 'date']
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'time': 'Время',
            'is_recurring': 'Повторяющаяся задача (как будильник)',
            'date': 'Дата (для разовой задачи)',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Например: Тренировка в зале'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Детали задачи...'
            }),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 'id': 'id_is_recurring'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk and instance.is_recurring:
            self.initial['repeat_days'] = [str(d) for d in instance.get_repeat_days_list()]

    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get('is_recurring')
        repeat_days = cleaned_data.get('repeat_days')
        date = cleaned_data.get('date')

        if is_recurring and not repeat_days:
            raise forms.ValidationError(
                'Выбери хотя бы один день недели для повторяющейся задачи.'
            )
        if not is_recurring and not date:
            raise forms.ValidationError(
                'Укажи дату для разовой (неповторяющейся) задачи.'
            )
        return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)
        if task.is_recurring:
            task.repeat_days = ','.join(self.cleaned_data['repeat_days'])
            task.date = None
        else:
            task.repeat_days = ''
        if commit:
            task.save()
        return task


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Имя пользователя'
        })
        self.fields['username'].help_text = None
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Пароль'
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Повторите пароль'
        })
        self.fields['password2'].help_text = None
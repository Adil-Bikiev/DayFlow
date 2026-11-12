from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, WEEKDAYS


class TaskForm(forms.ModelForm):
    repeat_days = forms.MultipleChoiceField(
        choices=[(str(k), v) for k, v in WEEKDAYS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Repeat on',
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'time', 'is_recurring', 'repeat_days', 'date']
        labels = {
            'title': 'Task title',
            'description': 'Description',
            'time': 'Time',
            'is_recurring': 'Recurring task (like an alarm)',
            'date': 'Date (for one-time tasks)',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Gym workout'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Task details...'
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
                'Choose at least one weekday for a recurring task.'
            )
        if not is_recurring and not date:
            raise forms.ValidationError(
                'Pick a date for a one-time task.'
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
            'class': 'form-control', 'placeholder': 'Username'
        })
        self.fields['username'].help_text = None
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Password'
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirm password'
        })
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Only @gmail.com addresses can be used to sign up.')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')

        return email
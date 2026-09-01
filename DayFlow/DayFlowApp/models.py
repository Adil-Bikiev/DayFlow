from django.contrib.auth.models import User
from django.db import models

WEEKDAYS = [
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
]

WEEKDAYS_SHORT = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}


class Task(models.Model):
    """Задача пользователя: разовая (на конкретную дату) либо
    повторяющаяся по дням недели (как будильник)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    time = models.TimeField('Время')

    is_recurring = models.BooleanField('Повторяющаяся задача', default=False)
    repeat_days = models.CharField(
        'Дни повтора',
        max_length=20,
        blank=True,
        help_text='Номера дней недели через запятую (0=Пн ... 6=Вс)',
    )
    date = models.DateField('Дата', null=True, blank=True)

    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def get_repeat_days_list(self):
        if not self.repeat_days:
            return []
        return [int(d) for d in self.repeat_days.split(',') if d != '']

    def repeat_days_display(self):
        days = self.get_repeat_days_list()
        return ' · '.join(WEEKDAYS_SHORT[d] for d in sorted(days))

    def occurs_on(self, some_date):
        """Проверяет, должна ли задача появиться в конкретный день."""
        if self.is_recurring:
            return some_date.weekday() in self.get_repeat_days_list()
        return self.date == some_date


class TaskCompletion(models.Model):
    """Отметка о выполнении задачи в конкретный день —
    нужна отдельно от Task, чтобы повторяющиеся задачи
    можно было отмечать выполненными индивидуально на каждый день."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('task', 'date')